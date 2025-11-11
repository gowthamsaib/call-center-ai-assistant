## Architecture

Client -> FastAPI -> Orchestrator -> Tools (mock CRM/KB/Ticket) -> Transcript -> Structured Extraction

This MVP runs synchronously. In production, the call execution would be handled by
an async worker (Celery/RQ/Kafka consumers) and integrated with telephony + STT/TTS providers.


## Architecture (MVP)

```mermaid
flowchart LR
  A[Client / Swagger / Streamlit] --> B[FastAPI /calls]
  B --> C[Orchestrator]
  C --> D[Voice Simulator]
  C --> E[Tools: CRM / KB / Ticket]
  C --> F[Extraction: Rule-based or LLM]
  C --> G[Store (in-memory)]
  C --> H[Metrics]
  B <-- G