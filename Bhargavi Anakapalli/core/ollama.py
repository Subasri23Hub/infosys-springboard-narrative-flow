# core/ollama.py — Ollama API helpers
import requests
import streamlit as st

from config.settings import OLLAMA_URL, OLLAMA_TAGS, MODELS, LENGTH_MAP


def check_ollama() -> tuple[bool, list[str]]:
    """Returns (running: bool, available_model_names: list)."""
    try:
        r = requests.get(OLLAMA_TAGS, timeout=2)
        if r.ok:
            tags = [m["name"].split(":")[0] for m in r.json().get("models", [])]
            return True, tags
    except Exception:
        pass
    return False, []


def call_ollama(messages: list[dict], extra_instruction: str = "") -> str:
    """
    Call Ollama /api/generate with the current model + settings.
    messages = [{"role": "user"|"assistant", "content": str}]
    """
    from core.prompts import build_system_prompt  # local import avoids circular

    system = build_system_prompt()
    if extra_instruction:
        system += f"\n\nSPECIAL TASK FOR THIS RESPONSE: {extra_instruction}"

    convo = ""
    for m in messages:
        role_label = "User" if m["role"] == "user" else "NarrativeFlow"
        convo += f"\n{role_label}: {m['content']}"
    convo += "\nNarrativeFlow:"

    full_prompt = f"<system>\n{system}\n</system>\n{convo}"

    payload = {
        "model":  st.session_state.model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": st.session_state.temperature,
            "num_predict": LENGTH_MAP.get(st.session_state.length_mode, 500),
        },
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        err_text = e.response.text
        return f"⚠️ Ollama {status} Error: {err_text}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot connect to Ollama. Make sure `ollama serve` is running."
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Try a shorter response length or a faster model."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
