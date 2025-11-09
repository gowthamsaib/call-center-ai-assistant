from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

# The OpenAI SDK reads OPENAI_API_KEY automatically if you don't pass api_key.
client = OpenAI()


def extract_with_llm(transcript_text: str, schema_fields: List[str]) -> Dict[str, Any]:
    """
    Extract structured fields from a transcript using OpenAI Structured Outputs (JSON Schema)
    via the Responses API. Returns a dict that conforms to the requested schema.

    Requirements:
      - OPENAI_API_KEY set in environment
      - USE_LLM_EXTRACTION=true (checked in orchestrator)
    """
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Build a strict JSON schema that contains ONLY the requested fields.
    properties: Dict[str, Any] = {}
    required: List[str] = []

    for f in schema_fields:
        required.append(f)
        # Add per-field types (extend these as your schema grows)
        if f == "duration_months":
            properties[f] = {"type": ["integer", "null"]}
        else:
            properties[f] = {"type": ["string", "null"]}

    json_schema = {
        "name": "call_extraction",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": properties,
            "required": required,
        },
    }

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "You extract structured fields from a call transcript. "
                    "Return ONLY valid JSON that matches the provided schema exactly."
                ),
            },
            {"role": "user", "content": transcript_text},
        ],
        # Structured Outputs in Responses API uses text.format (not response_format)
        text={"format": {"type": "json_schema", "json_schema": json_schema}},
    )

    # The SDK provides output_text as a safe aggregated text helper. :contentReference[oaicite:0]{index=0}
    raw = response.output_text
    if not raw:
        raise ValueError("No output_text returned from model.")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned non-JSON output: {raw[:200]}") from e

    # Final safety: ensure no extra keys sneak in
    for k in list(data.keys()):
        if k not in schema_fields:
            data.pop(k)

    # Ensure all keys exist (schema requires them); fill missing with None
    for k in schema_fields:
        data.setdefault(k, None)

    return data