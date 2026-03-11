# core/chat_utils.py — Chat history helpers
import streamlit as st
from datetime import datetime


def get_history() -> list[dict]:
    return st.session_state.chats.get(st.session_state.active_chat, [])


def add_message(role: str, content: str):
    chat = st.session_state.chats.setdefault(st.session_state.active_chat, [])
    chat.append({"role": role, "content": content, "ts": datetime.now().strftime("%H:%M")})
    # Auto-save session to disk
    try:
        from core.persistence import save_session
        if st.session_state.get("auth_username"):
            save_session(st.session_state.auth_username)
    except Exception:
        pass


def all_ai_text() -> str:
    return "\n\n".join(
        m["content"] for m in get_history() if m["role"] == "assistant"
    )


def word_count(text: str) -> int:
    return len(text.split()) if text.strip() else 0


def reading_time(wc: int) -> int:
    return max(1, round(wc / 200))


def get_flat_history() -> list[dict]:
    return [{"role": m["role"], "content": m["content"]} for m in get_history()]
