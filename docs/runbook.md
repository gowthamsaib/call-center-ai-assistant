## Runbook

This document describes common operational issues, debugging steps, and planned hardening work for the Call Center AI Assistant MVP.

---

## Service Overview

Components:

* Streamlit UI client
* FastAPI backend with calls API
* Call orchestrator for dialog management
* Mock CRM, knowledge base, and ticketing tools
* Transcript generation
* Structured field extraction
* In-memory call state storage
* Basic logging and metrics

Execution model:

* Synchronous execution
* Single-process runtime
* In-memory state only

---

## Common Issues and Resolutions

### API server not starting

Symptoms:

* Connection refused errors
* Streamlit unable to reach the backend

Checks:

* Confirm the virtual environment is activated
* Verify dependencies are installed
* Start the API manually

Command:

```
uvicorn app.main:app --reload
```

Fix:

```
pip install -e .[dev]
```

---

### Streamlit UI cannot submit calls

Symptoms:

* requests ConnectionError
* UI hangs after clicking Start Call

Checks:

* FastAPI is running
* API Base URL in Streamlit matches the FastAPI host and port

Fix:

```
streamlit run streamlit_app.py
```

Restart the FastAPI server before retrying.

---

### Repetitive or unnatural agent responses

Symptoms:

* Agent repeats the same confirmation message multiple times

Cause:

* Static acknowledgement logic in transcript generation

Fix:

* Use turn-aware acknowledgements
* Rotate or vary agent responses for follow-up turns
* Validate transcript output manually

---

### Incorrect or missing extracted fields

Symptoms:

* Missing fields in extracted JSON
* Incorrect values for duration, intent, or sentiment

Checks:

* Review transcript content
* Inspect extraction rules in the extraction logic

Fix:

* Update rule-based extraction logic
* Add or update unit tests for edge cases

---

### Tests failing

Symptoms:

* Local or CI test failures

Fix:

```
make test
```

Checks:

* Review recent orchestrator or extraction changes
* Ensure deterministic outputs for tests

---

### Unwanted files tracked in git

Symptoms:

* pycache, egg-info, or virtual environment files tracked

Fix:

* Ensure .gitignore includes:

```
__pycache__/
*.pyc
*.egg-info/
.venv/
```

Remove tracked files:

```
git rm -r --cached __pycache__ *.egg-info
```

---

## Debugging Tips

* Use the FastAPI docs endpoint to test the calls API
* Log transcripts before running extraction
* Validate in-memory call state during execution
* Restart both FastAPI and Streamlit after code changes

---

## Hardening Roadmap

Short term:

* Add async execution using a background worker
* Add retries and backoff for tool failures
* Improve logging and request tracing
* Add extraction confidence scoring

Medium term:

* Persist call state using SQLite or Postgres
* Replace rule-based extraction with LLM-based extraction
* Add API authentication
* Add rate limiting

Long term:

* Integrate real telephony providers
* Add speech-to-text and text-to-speech pipelines
* Introduce event streaming
* Add monitoring and model drift detection

---

## Operational Notes

* This MVP is not horizontally scalable
* All state is lost on restart
* Intended for local simulation and portfolio demonstration

---