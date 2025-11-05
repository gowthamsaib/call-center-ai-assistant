## Architecture

Client -> FastAPI -> Orchestrator -> Tools (mock CRM/KB/Ticket) -> Transcript -> Structured Extraction

This MVP runs synchronously. In production, the call execution would be handled by
an async worker (Celery/RQ/Kafka consumers) and integrated with telephony + STT/TTS providers.
