.PHONY: setup run test

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip
	. .venv/bin/activate && pip install -e .[dev]

run:
	. .venv/bin/activate && uvicorn app.main:app --reload --port 8000

test:
	. .venv/bin/activate && pytest -q