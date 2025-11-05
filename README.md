# Call Center AI Assistant (Local Simulation)

A production-style **Call Center AI** service you can run locally:
- Start a “call” via API
- Run a simulated multi-turn conversation
- Generate a transcript
- Extract structured fields (e.g., issue type, resolution, next steps)
- Track observability metrics (latency, failures, tool usage)

This repo demonstrates real-world patterns used in call-center automation:
API orchestration, agent/tool routing, structured extraction, and reliability basics.

## Use cases
- Membership cancellation / freeze requests
- Billing disputes
- Appointment scheduling
- General customer support triage & routing

## Architecture
- **FastAPI** provides `/calls` endpoints
- A lightweight **agent orchestrator** runs a conversation loop
- A **voice simulator** creates user turns.
- **Tools** simulate CRM lookup, ticket creation, and KB search
- **Metrics + structured logs** provide observability

## Quickstart
```bash
make setup
make run