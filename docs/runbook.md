## Runbook

Common issues:
- Tests failing: run `make test`
- Server not starting: check venv activation and `pip install -e .[dev]`
- Extraction wrong: update `_extract_fields` rules and add tests

Next hardening steps:
- Add async execution
- Add retries/backoff
- Add persistence (SQLite/Postgres)
- Add real LLM extraction
- Add real telephony adapter
