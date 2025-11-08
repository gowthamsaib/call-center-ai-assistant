import os
from typing import Any, Dict, List
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_with_llm(transcript_text: str, schema_fields: List[str]) -> Dict[str, Any]:
    """
    Uses OpenAI Structured Outputs to return JSON that matches a schema.
    Falls back is handled by caller.
    """
    # Build a strict JSON schema with only requested fields
    properties = {}
    required = []
    for f in schema_fields:
        required.append(f)
        if f in {"duration_months"}:
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

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    resp = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "Extract structured fields from the call transcript. "
                    "Return ONLY JSON that matches the provided schema."
                ),
            },
            {"role": "user", "content": transcript_text},
        ],
        text={"format": {"type": "json_schema", "json_schema": json_schema}},
    )

    # Responses API returns structured content in output_text for JSON schema mode
    # (the SDK parses it as text; we safely load it as JSON)
    import json
    return json.loads(resp.output_text)
