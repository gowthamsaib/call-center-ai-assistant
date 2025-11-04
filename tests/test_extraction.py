from app.agent.orchestrator import _extract_fields

def test_extract_fields_freeze():
    schema = ["issue_type","requested_action","duration_months","sentiment","resolution_summary","next_step"]
    text = "I want to freeze my membership for 3 months. Thanks."
    out = _extract_fields(text, schema)
    assert out["issue_type"] == "membership_freeze"
    assert out["duration_months"] == 3
    assert out["sentiment"] == "positive"
