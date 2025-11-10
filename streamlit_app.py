import requests
import streamlit as st

st.title("Call Center AI Assistant (Demo)")

base_url = st.text_input("API Base URL", "http://127.0.0.1:8000")

customer_name = st.text_input("Customer name", "Alex")
member_id = st.text_input("Member ID", "M-10293")
task = st.text_area("Task", "Freeze membership for 2 months due to travel")

schema = st.multiselect(
    "Fields to extract",
    ["issue_type","requested_action","duration_months","sentiment","resolution_summary","next_step"],
    default=["issue_type","requested_action","duration_months","sentiment","resolution_summary","next_step"],
)

if st.button("Start Call"):
    payload = {
        "customer_name": customer_name,
        "member_id": member_id,
        "task": task,
        "schema": schema,
    }
    r = requests.post(f"{base_url}/calls", json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()

    st.success(f"Call completed: {data['call_id']}")
    st.subheader("Extracted Fields")
    st.json(data["extracted_fields"])

    st.subheader("Transcript")
    for turn in data["transcript"]:
        st.markdown(f"**{turn['role'].upper()}**: {turn['text']}")
