SYSTEM_STYLE = (
    "You are a helpful call center assistant. Be concise, polite, and confirm details."
)

def opening(customer_name: str) -> str:
    return f"Hi {customer_name}, this is the support assistant. How can I help you today?"
