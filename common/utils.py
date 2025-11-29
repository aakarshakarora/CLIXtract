import json
import re
from pathlib import Path

from llm.client_factory import get_llm_client

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
SYSTEM_PROMPT_FILE = PROMPTS_DIR / "system_prompt.txt"

# Strip ``` or ```json fences
CODE_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


def _strip_code_fences(text: str) -> str:
    """Remove Markdown code fences but preserve inner content."""
    return CODE_FENCE_RE.sub(lambda m: m.group(1), text)


def extract_json(text: str):
    """
    Extract the first valid JSON object or array.
    If none found → return "[]".
    """
    if not text:
        return "[]"

    text_clean = _strip_code_fences(text).strip()

    # If the whole text is valid JSON, return it
    try:
        json.loads(text_clean)
        return text_clean
    except Exception:
        pass

    # Scan for balanced JSON substrings
    length = len(text_clean)
    for i, ch in enumerate(text_clean):
        if ch not in ("{", "["):
            continue

        stack = []
        start = i

        for j in range(i, length):
            c = text_clean[j]

            if c == "{":
                stack.append("}")
            elif c == "[":
                stack.append("]")
            elif c in ("}", "]"):
                if not stack:
                    break

                expected = stack.pop()
                if c != expected:
                    stack = []
                    break

                if not stack:
                    candidate = text_clean[start : j + 1].strip()
                    try:
                        json.loads(candidate)
                        return candidate
                    except Exception:
                        break

    # Regex fallback
    m = re.search(r"\[(?:.|\s)*?\]", text_clean)
    if m:
        candidate = m.group(0)
        try:
            json.loads(candidate)
            return candidate
        except Exception:
            pass

    m = re.search(r"\{(?:.|\s)*?\}", text_clean)
    if m:
        candidate = m.group(0)
        try:
            json.loads(candidate)
            return candidate
        except Exception:
            pass

    # No valid JSON → return empty array
    return "[]"


def safe_load_json(text: str):
    """Attempt to load JSON and return (object, error_or_none)."""
    try:
        obj = json.loads(text)
        return obj, None
    except Exception as e:
        return None, f"JSONDecodeError: {e}"


async def parse_cli_output(
    command_output: str,
    command_name: str = None,
    user_instruction: str = None,
    max_tokens: int = 2048,
):
    """
    Returns: (parsed_json, metadata)
    Guaranteed: parsed_json is ALWAYS a list (even if empty).
    """
    if not command_output:
        return [], {"error": "command_output is empty"}

    system_prompt = (
        SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
        if SYSTEM_PROMPT_FILE.exists()
        else ""
    )

    # Build user prompt
    prompt = "\n\n".join(
        [
            system_prompt.strip(),
            f"COMMAND_NAME: {command_name or 'unknown'}",
            "CLI_OUTPUT:",
            command_output.strip(),
            "INSTRUCTION:",
            (
                user_instruction.strip()
                if user_instruction
                else "Return structured JSON array only."
            ),
        ]
    )

    client = get_llm_client()

    # Generate response
    try:
        raw = client.generate(prompt, max_tokens=max_tokens)
    except Exception as e:
        return [], {"error": f"LLM generation failed: {e}", "prompt": prompt}

    # Extract JSON
    json_text = extract_json(raw)

    # Parse JSON
    parsed, load_err = safe_load_json(json_text)
    if load_err:
        return [], {
            "error": "Failed to parse JSON from LLM",
            "load_error": load_err,
            "json_text": json_text,
            "raw_response": raw,
            "prompt": prompt,
        }

    # Guarantee list output
    if not isinstance(parsed, list):
        parsed = [parsed]

    return parsed, {
        "raw_response": raw,
        "json_text": json_text,
        "prompt": prompt,
    }
