from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_call():
    payload = {
        "customer_name": "Alex",
        "member_id": "M-10293",
        "task": "Freeze membership for 2 months due to travel",
        "schema": ["issue_type","requested_action","duration_months","sentiment","resolution_summary","next_step"]
    }
    r = client.post("/calls", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "completed"
    assert data["extracted_fields"]["issue_type"] == "membership_freeze"
    assert data["extracted_fields"]["duration_months"] == 2

    call_id = data["call_id"]
    r2 = client.get(f"/calls/{call_id}")
    assert r2.status_code == 200
