# core/persistence.py — File-based session persistence
import json
import os

SESSION_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sessions")
ACTIVE_FILE = os.path.join(SESSION_DIR, "_active.txt")

# Keys we persist per user
_PERSIST_KEYS = [
    "logged_in", "auth_user_id", "auth_username", "auth_bio", "auth_pic",
    "_profile_synced", "user_profile",
    "chats", "active_chat", "active_story_id", "chat_counter", "current_page",
    "model", "temperature", "length_mode",
    "genre", "tone", "writing_style",
    "story_context", "response_mode", "memory_mode", "auto_continue",
    "ui_theme", "font_size", "bubble_style",
    "split_draft", "outline", "chapter_count",
    "right_sidebar_open",
]


def _ensure_dir():
    os.makedirs(SESSION_DIR, exist_ok=True)


def save_session(username: str):
    """Save the current session state to a JSON file for the given user."""
    import streamlit as st
    _ensure_dir()
    data = {}
    for key in _PERSIST_KEYS:
        val = st.session_state.get(key)
        # Skip binary data (profile pics) — not JSON-serializable
        if key == "auth_pic" and val is not None:
            continue
        if key == "user_profile" and isinstance(val, dict):
            val = {k: v for k, v in val.items() if k != "profile_pic"}
        data[key] = val

    path = os.path.join(SESSION_DIR, f"{username}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_session(username: str) -> dict | None:
    """Load a previously saved session for the given user. Returns None if not found."""
    path = os.path.join(SESSION_DIR, f"{username}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Re-add profile_pic placeholder
        if "user_profile" in data and isinstance(data["user_profile"], dict):
            data["user_profile"].setdefault("profile_pic", None)
        return data
    except (json.JSONDecodeError, IOError):
        return None


def save_active_user(username: str):
    """Remember who is currently logged in (survives page refresh)."""
    _ensure_dir()
    with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
        f.write(username)


def load_active_user() -> str | None:
    """Return the last logged-in username, or None."""
    if not os.path.exists(ACTIVE_FILE):
        return None
    try:
        with open(ACTIVE_FILE, "r", encoding="utf-8") as f:
            name = f.read().strip()
        return name if name else None
    except IOError:
        return None


def clear_active_user():
    """Clear the active-user token (called on logout)."""
    if os.path.exists(ACTIVE_FILE):
        os.remove(ACTIVE_FILE)
