import json
from pathlib import Path

from llm.providers.ollama_client import OllamaClient

SETTINGS_PATH = Path(__file__).resolve().parents[1] / "settings.json"


def _load_settings():
    if not SETTINGS_PATH.exists():
        raise FileNotFoundError(f"Settings file not found at {SETTINGS_PATH}")
    with SETTINGS_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def get_llm_client():
    settings = _load_settings()
    llm_settings = settings.get("llm_settings", {})
    default = llm_settings.get("default", "ollama").lower()

    match default:
        case "ollama":
            cfg = llm_settings.get("ollama", {})
            print(cfg)
            model = cfg.get("model", "llama3")
            temperature = cfg.get("temperature", 0)

            return OllamaClient(model=model, temperature=temperature)

        case _:
            raise ValueError(
                f"Unsupported LLM provider specified in settings: {default}"
            )
