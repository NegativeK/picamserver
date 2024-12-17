types:
	./venv/bin/mypy *.py

lint:
	./venv/bin/ruff check

static_checking: lint types
