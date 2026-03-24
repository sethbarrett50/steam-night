SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

UV    ?= uv
RUFF  ?= ruff
PY    ?= python

HOST      ?= 0.0.0.0
PORT      ?= 5000
PASSWORD  ?= dragon
TARGET    ?= http://127.0.0.1:5000
DELAY     ?= 0.1
WORDLIST  ?= assets/wordlists/demo_passwords.txt

.PHONY: help sync format check lint test build clean \
        run-cyber-server run-cyber-crack run-cs \
        debug-imports preflight

help: ## Show targets
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

sync: ## Install/sync deps including dev dependencies
	$(UV) sync --dev

format: ## Format code
	$(UV) run $(RUFF) format .

check: ## Lint without fixes
	$(UV) run $(RUFF) check .

lint: ## Format + lint with fixes
	$(UV) run $(RUFF) format .
	$(UV) run $(RUFF) check . --fix

test: ## Run tests
	$(UV) run pytest -q

build: ## Build sdist and wheel
	$(UV) build

clean: ## Remove common build/cache artifacts
	rm -rf dist build .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.egg-info' -prune -exec rm -rf {} +

debug-imports: ## Check whether local packages are importable
	$(UV) run $(PY) -c "import cyber; print('cyber:', cyber.__file__)"
	$(UV) run $(PY) -c "import cs; print('cs:', cs.__file__)"

run-cyber-server: ## Run the Raspberry Pi cyber demo server
	$(UV) run cyber-server --host $(HOST) --port $(PORT) --password $(PASSWORD)

run-cyber-crack: ## Run the laptop-side dictionary attack demo
	$(UV) run cyber-crack --target $(TARGET) --delay $(DELAY) --wordlist $(WORDLIST)

run-cs: ## Run the CS demo placeholder
	$(UV) run cs-demo

preflight: ## Build package and run metadata checks
	$(UV) build
	uvx twine check dist/*