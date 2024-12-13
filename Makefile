VENV := . venv/bin/activate

types:
	${VENV} && mypy *.py
	
lint:
	${VENV} && ruff check

static_checking: lint types
