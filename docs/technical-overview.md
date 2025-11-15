## Technical Deep Dive

This document explains how the Call Center AI Assistant works internally, from request intake to response generation.

It is intended for engineers and technical reviewers.

---

## High-Level Architecture

The system is composed of the following layers:

- Client Layer
  Streamlit UI and Swagger API interface

- API Layer
  FastAPI backend exposing call-related endpoints

- Orchestration Layer
  Core logic managing the conversation flow and tool usage

- Tool Layer
  Mock CRM, knowledge base, and ticketing services

- Extraction Layer
  Converts conversation transcripts into structured fields

- Storage Layer
  In-memory storage for call state and results

- Observability
  Basic metrics and logging hooks

---

## Request Flow

1. A client submits a request to the calls API.
2. The API validates the input and invokes the orchestrator.
3. The orchestrator initializes call context.
4. Mock tools are queried for customer and policy information.
5. A multi-turn conversation transcript is generated.
6. Structured extraction logic parses the transcript.
7. A support ticket is created.
8. Results are stored in memory.
9. The final response is returned to the client.

---

## Conversation Management

The conversation is simulated using deterministic logic:
- Initial greeting
- Intent confirmation
- Follow-up acknowledgements
- Request completion and closure

Acknowledgement responses are varied to improve realism while remaining deterministic for testing.

---

## Extraction Strategy

Two extraction approaches are supported:

- Rule-based extraction (default)
  Deterministic, testable, and runs without external dependencies.

- LLM-based extraction (optional)
  Uses a large language model with strict schema enforcement.
  Disabled by default and safely gated via environment variables.

A fallback mechanism ensures the system always returns valid output.

---

## Data Storage

All call data is stored in memory for simplicity:
- Call request
- Transcript
- Extracted fields
- Basic metrics

This design prioritizes clarity and ease of understanding.

---

## Testing and Reliability

- Unit tests validate API behavior and extraction logic.
- Deterministic outputs ensure repeatable test results.
- GitHub Actions runs tests automatically on each commit.

---

## Limitations

This is a demonstration system:
- No persistent storage
- No real telephony integration
- No authentication or authorization
- Single-process execution

These constraints are intentional to keep the project lightweight.

---

## Future Improvements

Potential extensions include:
- Asynchronous execution
- Persistent storage
- Real CRM and ticketing integrations
- Telephony and speech processing
- Advanced monitoring and alerting

---

## Summary

From a technical perspective, this project demonstrates how to design an AI-assisted workflow system that is modular, testable, and representative of real-world production architectures, while remaining accessible and easy to run locally.