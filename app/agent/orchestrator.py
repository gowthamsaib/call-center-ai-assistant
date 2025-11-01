from __future__ import annotations

import re
from typing import Any, Dict, List

from app.agent.schemas import CallRequest, CallResult, Turn
from app.agent.prompts import opening
from app.voice.simulator import simulate_user_turns
from app.agent import tools


def extract_fields(transcript_text: str, schema: List[str]) -> Dict[str, Any]:
    """
    Deterministic extraction to keep the repo runnable + testable.
    (Can later swap this with LLM-based extraction.)
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
    elif any(w in text for w in ["billing", "charge", "refund"]):
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
        if any(w in text for w in ["thanks", "thank you", "great"]):
            fields["sentiment"] = "positive"
        elif any(w in text for w in ["angry", "upset", "frustrated"]):
            fields["sentiment"] = "negative"
        else:
            fields["sentiment"] = "neutral"

    # Resolution / next steps
    if "resolution_summary" in fields:
        fields["resolution_summary"] = (
            "Captured the request, validated basic account context, and created a support ticket."
        )
    if "next_step" in fields:
        fields["next_step"] = "Support team will confirm the update within 24 hours."

    return fields


def run_call(call_id: str, req: CallRequest, store, metrics) -> CallResult:
    """
    Runs a simulated call end-to-end.
    For the MVP, this is synchronous. In a real system this would run in a worker.
    """
    transcript: List[Turn] = []
    tool_calls = 0

    # Opening
    transcript.append(Turn(role="agent", text=opening(req.customer_name)))

    # Simulated user turns (stand-in for STT output)
    user_turns = simulate_user_turns(req.task)

    # Tool usage (realistic order: CRM -> KB -> ticket)
    crm = tools.crm_lookup(req.member_id)
    tool_calls += 1

    kb = tools.kb_search(req.task)
    tool_calls += 1

    for user_text in user_turns:
        transcript.append(Turn(role="user", text=user_text))

        agent_text = (
            f"Understood. I can help with that. I see your account is **{crm['status']}** on the "
            f"**{crm['plan']}** plan. Policy reference: **{kb['top_article']}**. "
            "I’ll submit the request now."
        )
        transcript.append(Turn(role="agent", text=agent_text))

    ticket = tools.create_ticket(req.member_id, "member_request", req.task)
    tool_calls += 1

    transcript.append(
        Turn(
            role="agent",
            text=f"Request created successfully. Ticket ID: **{ticket['ticket_id']}**. "
                 "Is there anything else I can help you with?"
        )
    )

    transcript_text = " ".join(t.text for t in transcript)
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