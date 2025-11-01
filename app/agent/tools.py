from typing import Dict, Any

def crm_lookup(member_id: str) -> Dict[str, Any]:
    # Mock CRM data
    return {"member_id": member_id, "status": "active", "plan": "premium", "tenure_months": 14}

def kb_search(query: str) -> Dict[str, Any]:
    # Mock knowledge base
    return {"top_article": "Membership Freeze Policy", "notes": "Freeze allowed up to 3 months with active account."}

def create_ticket(member_id: str, issue: str, details: str) -> Dict[str, Any]:
    # Mock ticketing
    return {"ticket_id": f"T-{member_id[-4:]}-001", "issue": issue, "status": "created"}
