# Python executable and venv
PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin

# Windows fallback (optional)
ifeq ($(OS),Windows_NT)
	PYTHON := python
	BIN := $(VENV)/Scripts
endif

# ------------------------------------
# Create virtual environment and install deps
# ------------------------------------
prepare-venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing dependencies..."
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt || true
	@echo "Venv ready."

# ------------------------------------
# Format code using isort + black
# ------------------------------------
format:
	$(BIN)/isort .
	$(BIN)/black .

# ------------------------------------
# Clean temporary files & venv
# ------------------------------------
clean:
	@echo "Cleaning temp files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ .pytest_cache/ $(VENV)

# ------------------------------------
# Run FastAPI server using host/port from settings.json via jq
# ------------------------------------
run-server:
	@echo "Starting FastAPI server..."
	@HOST=$$(jq -r '.api_settings.host // "0.0.0.0"' settings.json); \
	PORT=$$(jq -r '.api_settings.port // 8000' settings.json); \
	echo "Using host=$$HOST port=$$PORT"; \
	$(BIN)/uvicorn main:app --reload --host $$HOST --port $$PORT

# ------------------------------------
# Help
# ------------------------------------
help:
	@echo "Available commands:"
	@echo "  make prepare-venv   - Create virtual environment"
	@echo "  make format         - Format code with isort + black"
	@echo "  make clean          - Remove temp files and venv"
	@echo "  make run-server     - Run FastAPI server (host/port from settings.json)"