from __future__ import annotations

import os
import re
from typing import Any, Dict, List

from app.agent.schemas import CallRequest, CallResult, Turn
from app.agent.prompts import opening
from app.voice.simulator import simulate_user_turns
from app.agent import tools


def extract_fields(transcript_text: str, schema: List[str]) -> Dict[str, Any]:
    """
    Deterministic extraction (testable, local-only).
    Keep this as a fallback even if you enable LLM extraction.
    """
    fields: Dict[str, Any] = {k: None for k in schema}
    text = transcript_text.lower()

    # Issue classification
    if "freeze" in text:
        fields["issue_type"] = "membership_freeze"
        if "requested_action" in fields:
            fields["requested_action"] = "freeze_membership"
    elif "cancel" in text:
        fields["issue_type"] = "membership_cancellation"
        if "requested_action" in fields:
            fields["requested_action"] = "cancel_membership"
    elif any(w in text for w in ["billing", "charge", "refund", "payment"]):
        fields["issue_type"] = "billing_issue"
        if "requested_action" in fields:
            fields["requested_action"] = "review_billing"
    else:
        fields["issue_type"] = "general_support"
        if "requested_action" in fields:
            fields["requested_action"] = "investigate_request"

    # Duration months (optional)
    if "duration_months" in fields:
        m = re.search(r"(\d+)\s*month", text)
        if m:
            fields["duration_months"] = int(m.group(1))

    # Sentiment (simple heuristic)
    if "sentiment" in fields:
        if any(w in text for w in ["thanks", "thank you", "great", "awesome"]):
            fields["sentiment"] = "positive"
        elif any(w in text for w in ["angry", "upset", "frustrated", "disappointed"]):
            fields["sentiment"] = "negative"
        else:
            fields["sentiment"] = "neutral"

    # Resolution / next steps
    if "resolution_summary" in fields:
        fields["resolution_summary"] = (
            "Captured the request, validated account context, and created a support ticket."
        )
    if "next_step" in fields:
        fields["next_step"] = "Support team will confirm the update within 24 hours."

    return fields


def _maybe_llm_extract(transcript_text: str, schema: List[str]) -> Dict[str, Any] | None:
    """
    Optional LLM extraction (enabled via env).
    Returns None if disabled or if anything fails.
    """
    use_llm = os.getenv("USE_LLM_EXTRACTION", "false").strip().lower() == "true"
    if not use_llm:
        return None

    # If they enable it but forgot the key, just safely fall back
    if not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        # Import only when needed so the repo runs without OpenAI installed
        from app.agent.llm_extractor import extract_with_llm  # type: ignore

        return extract_with_llm(transcript_text, schema)
    except Exception:
        # Never break the call flow just because LLM extraction failed
        return None


def run_call(call_id: str, req: CallRequest, store, metrics) -> CallResult:
    """
    Runs a simulated call end-to-end.
    For MVP, synchronous execution. In production, run via a worker/queue.
    """
    transcript: List[Turn] = []
    tool_calls = 0

    # Opening
    transcript.append(Turn(role="agent", text=opening(req.customer_name)))

    # Simulated user turns (stand-in for STT transcripts)
    user_turns = simulate_user_turns(req.task)

    # Tools (realistic order)
    crm = tools.crm_lookup(req.member_id)
    tool_calls += 1

    kb = tools.kb_search(req.task)
    tool_calls += 1

    # Conversation loop
    agent_text = (
        f"Understood. I can help with that. I see your account is {crm['status']} on the "
        f"{crm['plan']} plan. Policy reference: {kb['top_article']}. "
        "I’ll submit the request now."
    )

    for i, user_text in enumerate(user_turns):
        transcript.append(Turn(role="user", text=user_text))

        if i == 0:
            # Full confirmation only once
            transcript.append(Turn(role="agent", text=agent_text))
        else:
            ACKS = [
                "Thanks for confirming.",
                "Got it.",
                "Understood.",
                "Perfect, thanks.",
                "All set."
            ]
            transcript.append(
                Turn(role="agent", text=ACKS[i % len(ACKS)])
            )



    # Ticket creation
    ticket = tools.create_ticket(req.member_id, "member_request", req.task)
    tool_calls += 1

    transcript.append(
        Turn(
            role="agent",
            text=f"Request created successfully. Ticket ID: {ticket['ticket_id']}. "
                 "Is there anything else I can help you with?"
        )
    )

    transcript_text = " ".join(t.text for t in transcript)

    # Extraction (LLM if enabled, else deterministic; always safe fallback)
    extracted = _maybe_llm_extract(transcript_text, req.schema)
    if extracted is None:
        extracted = extract_fields(transcript_text, req.schema)

    # Observability metrics
    metrics.inc("tool_calls_total", tool_calls)
    metrics.inc("calls_completed_total", 1)

    return CallResult(
        transcript=transcript,
        extracted_fields=extracted,
        tool_calls=tool_calls,
        fallback_rate=0.0,
    )