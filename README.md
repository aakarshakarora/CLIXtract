# CLIXtract

CLIXtract is a deterministic CLI parsing engine for network devices. It converts raw CLI output into structured JSON
using a local LLM (Ollama). The system is designed to extract only explicitly present fields and never invent data.
Missing values are returned as `"N/A"`.

---

## Project Structure

```
Makefile                 # Build and utility commands
common/                  # Shared utilities and helpers
llm/                     # LLM clients and wrappers
main.py                  # FastAPI server entry point
prompts/                 # System prompts and instructions
postman/                 # Example Postman requests
requirements.txt         # Python dependencies
schema/                  # JSON schemas (optional)
settings.json            # Configuration for LLM, server, and models
TODO.txt                 # Notes and tasks
version.json             # Project version info
```

---

## Prerequisites

- Python 3.12+
- Ollama installed and model downloaded (e.g., `llama3.1:latest`)
- macOS/Linux (Metal GPU recommended)
- `pip` for Python dependencies

---

## Setup

1. **Create virtual environment and install dependencies:**

```bash
make prepare-venv
```

2. **Start Ollama server:**

```bash
ollama serve
```

Check that your model is available:

```bash
ollama list
```

---

## Makefile Commands

- **Format code:**

```bash
make format
```

Formats Python code with `black` and `isort`.

- **Clean project:**

```bash
make clean
```

Removes temporary files and virtual environment.

- **Prepare virtual environment:**

```bash
make prepare-venv
```

- **Run FastAPI server:**

```bash
make run-server
```

Server port is picked from `settings.json`.

---

## API

**Endpoint:** `/parse-cli`  
**Method:** `POST`  
**Content-Type:** `application/json`

### Request Payload

Example for `show version`:

```json
{
  "command_name": "show version",
  "command_output": "Cisco IOS Software, C3750X Software (C3750X-UNIVERSALK9-M), Version 15.2(6)E2, RELEASE SOFTWARE ...",
  "user_instruction": "Extract software version (sw), firmware version (fw), hardware type, IOS version, system serial number, system image. Return strictly valid JSON. Use 'N/A' if not available."
}
```

Example for `show interface`:

```json
{
  "command_name": "show interface",
  "command_output": "GigabitEthernet1/0/1 is up, line protocol is up\n  Hardware is Gigabit Ethernet, address is 001a.2b3c.4d5e (bia 001a.2b3c.4d5e)\n  MTU 1500 bytes, BW 1000 Mbps, DLY 10 usec, ...",
  "user_instruction": "Extract interface name, status, protocol, hardware, MAC address, MTU, bandwidth. Return strictly valid JSON. Use 'N/A' if not available."
}
```

---

### Response Example

```json
{
  "sw": "C3750X Software (C3750X-UNIVERSALK9-M)",
  "fw": "N/A",
  "hardware": "WS-C3750X-24T-S",
  "ios_version": "15.2(6)E2",
  "serial_number": "FDO12345678",
  "system_image": "flash:c3750x-universalk9-mz.152-6.E2.bin"
}
```

---

## Prompts

- System prompts are in `prompts/system_prompt.txt`.
- They define parsing rules and instructions for the LLM.
- Always returns a **strict JSON array**, or an empty array `[]` if no valid objects are found.

---

## Notes

- Only strictly present fields in CLI output are included; missing fields return `"N/A"`.
- LLM client settings are configured via `settings.json`.
- FastAPI server returns JSON for any network CLI command provided.

---

## Postman

The `postman/` folder contains example requests you can import to test the API.

---

## TODO

See `TODO.txt` for ongoing tasks and improvements.

---


