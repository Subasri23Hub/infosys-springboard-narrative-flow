# core/state.py — Session state initialization
import streamlit as st


def init_state():
    """Initialize all Streamlit session state defaults (idempotent).
    On first load, checks for a previously active user and restores their session."""
    defaults = {
        # ── Chat ──
        "chats":        {"Story 1": []},
        "active_chat":  "Story 1",
        "chat_counter": 1,

        # ── Ollama Model Settings ──
        "model":        "llama3:latest",
        "temperature":  0.7,
        "length_mode":  "Medium",

        # ── User Profile ──
        "user_profile": {
            "username":    "Guest User",
            "password":    "password",
            "bio":         "I love creating amazing stories.",
            "profile_pic": None,
        },
        "current_page": "💬 Story Chat",

        # ── Story Customization ──
        "genre":         "Fantasy",
        "tone":          "Dramatic",
        "writing_style": "Descriptive",

        # ── Character & World ──
        "story_context": {
            "title":             "",
            "char_name":         "",
            "char_personality":  ["Brave"],
            "perspective":       "Third person",
            "setting":           "",
        },

        # ── Chat Behavior ──
        "response_mode": "Detailed narration",
        "memory_mode":   "Session only",
        "auto_continue": False,

        # ── UI Preferences ──
        "ui_theme":    "Dark",
        "font_size":   15,
        "bubble_style":"Glass style",

        # ── Tools ──
        "split_draft":   "",
        "outline":       [],
        "chapter_count": 1,

        # ── Future Hooks ──
        "voice_input_enabled": False,
        "tts_enabled":         False,

        # ── Right Sidebar ──
        "right_sidebar_open": False,

        # ── Auth ──
        "logged_in":       False,
        "auth_user_id":    None,
        "auth_username":   "",
        "auth_bio":        "",
        "auth_pic":        None,
        "_profile_synced": False,

        # ── Chapter-based Story Editor ──
        "story_title":       "Untitled Story",
        "chapters":          {"Chapter 1": ""},   # chapter_name -> content
        "active_chapter":    "Chapter 1",
        "chapter_order":     ["Chapter 1"],       # ordered list
        "chapter_counter":   1,

        # ── Story Search & Tags ──
        "search_story":      "",
        "story_tags":        {},                  # story_name -> list of tags

        # ── AI Suggestion (latest) ──
        "last_ai_suggestion": "",
        # ── Story Metadata (Title, Pinned) ──
        "story_metadata":    {"Story 1": {"title": "Untitled Story", "pinned": False}},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Ensure all existing chats have metadata
    if "story_metadata" not in st.session_state:
        st.session_state.story_metadata = {}
    for chat_name in st.session_state.chats:
        if chat_name not in st.session_state.story_metadata:
            st.session_state.story_metadata[chat_name] = {"title": chat_name, "pinned": False}

    # ── RESTORE PERSISTED SESSION ──
    # Only attempt restore once per Streamlit session
    if "_session_restored" not in st.session_state:
        st.session_state._session_restored = True
        try:
            from core.persistence import load_active_user, load_session
            active_user = load_active_user()
            if active_user:
                saved = load_session(active_user)
                if saved and saved.get("logged_in"):
                    for key, val in saved.items():
                        st.session_state[key] = val
                    # Ensure profile_pic placeholder exists
                    if "user_profile" in saved and isinstance(saved["user_profile"], dict):
                        st.session_state.user_profile.setdefault("profile_pic", None)
        except Exception:
            pass  # If persistence fails, fall back to fresh state


def sync_profile_after_login():
    """Copy auth data into user_profile on the first run after login, and load stories."""
    if not getattr(st.session_state, "_profile_synced", False):
        st.session_state.user_profile["username"]    = st.session_state.auth_username
        st.session_state.user_profile["bio"]         = st.session_state.auth_bio or "I love creating amazing stories."
        st.session_state.user_profile["profile_pic"] = st.session_state.auth_pic
        
        # --- DB Load (Only if session chats are empty default mock) ---
        user_id = getattr(st.session_state, "auth_user_id", None)
        
        if not user_id and getattr(st.session_state, "logged_in", False) and getattr(st.session_state, "auth_username", ""):
            from database.database import SessionLocal
            from services import auth_service
            db = SessionLocal()
            user = auth_service.get_user_by_username(db, st.session_state.auth_username)
            if user:
                 user_id = user.id
                 st.session_state.auth_user_id = user_id
            db.close()
            
        if user_id and list(st.session_state.chats.keys()) == ["Story 1"] and not st.session_state.chats["Story 1"]:
            from database.database import SessionLocal
            from services import story_service, chat_service
            db = SessionLocal()
            stories = story_service.get_stories_by_user(db, user_id)
            if stories:
                # Clear default mock story
                st.session_state.chats = {}
                st.session_state.story_metadata = {}
                
                # Load stories into session state
                for story in reversed(stories): # oldest first, so newest is active
                    name = f"Story_{story.id}"
                    flat_chats = []
                    for c in chat_service.get_chat_history(db, story.id):
                        flat_chats.append({"role": c.role, "content": c.message, "ts": str(c.timestamp.strftime("%H:%M") if c.timestamp else "")})
                    
                    st.session_state.chats[name] = flat_chats
                    last_up = str(story.updated_at.strftime("%b %d, %H:%M")) if story.updated_at else ""
                    st.session_state.story_metadata[name] = {"title": story.title, "pinned": False, "db_id": story.id, "last_updated": last_up}
                    
                    # Store chapter content temporarily in metadata so we can load it if selected later
                    st.session_state.story_metadata[name]["content"] = story.content or ""
                
                # Set active to the most recent (which was first in `stories` due to order_by desc)
                active_story = stories[0]
                active_name = f"Story_{active_story.id}"
                st.session_state.active_chat = active_name
                st.session_state.story_title = active_story.title
                st.session_state.chapters = {"Chapter 1": active_story.content or ""}
                st.session_state.chapter_order = ["Chapter 1"]
                st.session_state.active_chapter = "Chapter 1"
                st.session_state.active_story_id = active_story.id
                st.session_state.chat_counter = max(st.session_state.get("chat_counter", 0), len(stories))
            db.close()
            
        st.session_state._profile_synced = True
