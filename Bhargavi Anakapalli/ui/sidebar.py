# ui/sidebar.py — Left Streamlit sidebar
import streamlit as st

from core.ollama import check_ollama, call_ollama
from core.chat_utils import get_flat_history, add_message
from config.settings import MODELS, GENRES, TONES, STYLES, QUICK_STARTERS
from database.database import SessionLocal
from services import auth_service


def render_sidebar():
    with st.sidebar:

        # ── USER PROFILE ──
        prof = st.session_state.user_profile
        if "editing_profile" not in st.session_state:
            st.session_state.editing_profile = False

        st.markdown('<div class="section-lbl" style="margin-top:0; color:#bca06f; letter-spacing:0.1em;">USER PROFILE</div>',
                    unsafe_allow_html=True)

        if st.session_state.editing_profile:
            with st.form("edit_profile_form"):
                new_username = st.text_input("Username", value=prof["username"])
                new_bio      = st.text_area("Bio",       value=prof.get("bio", ""))
                new_pic      = st.file_uploader("Profile Picture", type=["png","jpg","jpeg"])

                if st.form_submit_button("Save"):
                    st.session_state.user_profile["username"] = new_username
                    st.session_state.user_profile["bio"]      = new_bio
                    if new_pic:
                        st.session_state.user_profile["profile_pic"] = new_pic.getvalue()
                    
                    db = SessionLocal()
                    user = auth_service.get_user_by_username(db, st.session_state.auth_username)
                    if user:
                        # Update user bio (profile pic is local only)
                        user.bio = new_bio
                        user.username = new_username
                        db.commit()
                        st.session_state.auth_username = new_username
                        st.session_state.auth_bio = new_bio
                    db.close()
                    
                    st.session_state.editing_profile   = False
                    st.rerun()

            if st.button("Cancel", key="cancel_edit_sidebar", use_container_width=True):
                st.session_state.editing_profile = False
                st.rerun()
        else:
            pc1, pc2 = st.columns([1, 2])
            with pc1:
                if prof.get("profile_pic"):
                    st.image(prof["profile_pic"], use_container_width=True)
                else:
                    st.markdown(
                        "<div style='font-size:2.8rem;text-align:center;background:rgba(139,92,246,0.2);"
                        "border-radius:50%;width:55px;height:55px;display:flex;align-items:center;"
                        "justify-content:center;margin:0 auto;color:#8b5cf6;'>👤</div>",
                        unsafe_allow_html=True,
                    )
            with pc2:
                st.markdown(f"<div style='font-weight:bold;font-size:1.1em;margin-bottom:4px;color:var(--text);'>"
                            f"{prof.get('username')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.85em;color:var(--muted);line-height:1.3;'>"
                            f"{prof.get('bio','')}</div>", unsafe_allow_html=True)

            st.write("")
            st.markdown('<div class="profile-actions">', unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Edit", key="edit_sidebar", use_container_width=True):
                    st.session_state.editing_profile = True
                    st.rerun()
            with b2:
                if st.button("Log out", key="logout_sidebar", use_container_width=True, type="primary"):
                    try:
                        from core.persistence import clear_active_user
                        clear_active_user()
                    except Exception:
                        pass
                    for key in ["logged_in","auth_username","auth_bio","auth_pic","auth_user_id",
                                "_profile_synced","editing_profile","right_sidebar_open",
                                "active_story_id", "search_story"]:
                        st.session_state[key] = (
                            False if key == "logged_in" else
                            "" if "username" in key or "bio" in key or "search" in key else
                            None if "pic" in key or "id" in key else False
                        )
                    st.session_state.chats = {"Story 1": []}
                    st.session_state.story_metadata = {"Story 1": {"title": "Untitled Story", "pinned": False}}
                    st.session_state.active_chat = "Story 1"
                    st.session_state.chapters = {"Chapter 1": ""}
                    st.session_state.chapter_order = ["Chapter 1"]
                    st.session_state.active_chapter = "Chapter 1"
                    st.session_state.story_title = "Untitled Story"
                    st.session_state.chat_counter = 1
                    st.session_state.user_profile = {"username":"Guest User","bio":"","profile_pic":None}
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # ── New Story ──
        st.markdown('<div class="new-story-btn">', unsafe_allow_html=True)
        if st.button("＋  New Story", use_container_width=True):
            st.session_state.chat_counter += 1
            name = f"Story {st.session_state.chat_counter}"
            title = f"Untitled Story {st.session_state.chat_counter}"
            st.session_state.chats[name] = []
            st.session_state.story_metadata[name] = {"title": title, "pinned": False}
            st.session_state.active_chat = name
            # Reset chapters for new story
            st.session_state.story_title    = f"Untitled Story {st.session_state.chat_counter}"
            st.session_state.chapters       = {"Chapter 1": ""}
            st.session_state.chapter_order  = ["Chapter 1"]
            st.session_state.chapter_counter = 1
            st.session_state.active_chapter = "Chapter 1"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Search Stories ──
        st.markdown('<div class="section-lbl">🔍 Search Stories</div>', unsafe_allow_html=True)
        search_val = st.text_input(
            "Search story history",
            value=st.session_state.get("search_story", ""),
            placeholder="Search story history…",
            label_visibility="collapsed",
            key="search_story_input",
        )
        st.session_state.search_story = search_val

        # ── Story History ──
        st.markdown('<div class="section-lbl">📚 History</div>', unsafe_allow_html=True)
        all_chats = list(reversed(list(st.session_state.chats.keys())))
        
        # Filter by search
        if search_val:
            filtered = []
            for c in all_chats:
                title = st.session_state.story_metadata.get(c, {}).get("title", c)
                if search_val.lower() in title.lower():
                    filtered.append(c)
        else:
            filtered = all_chats

        if not filtered:
            st.markdown('<div style="font-size:0.8rem;color:var(--muted);padding:0.3rem 0;">No stories found.</div>', unsafe_allow_html=True)
        else:
            # Separate pinned from unpinned
            pinned_chats = [c for c in filtered if st.session_state.story_metadata.get(c, {}).get("pinned", False)]
            unpinned_chats = [c for c in filtered if not st.session_state.story_metadata.get(c, {}).get("pinned", False)]
            
            # Scrollable container for history
            with st.container(height=350, border=False):
                # Helper to render a single history row
                def render_history_row(chat_id):
                    is_active = chat_id == st.session_state.active_chat
                    meta = st.session_state.story_metadata.get(chat_id, {"title": chat_id, "pinned": False})
                    
                    # Layout: button (left) | popover (right)
                    col_btn, col_menu = st.columns([5, 1], vertical_alignment="center")
                    
                    with col_btn:
                        btn_label = ("▸ " if is_active else "  ") + meta["title"]
                        last_up = meta.get("last_updated", "")
                        display_text = f"{btn_label}<br><span style='font-size:0.65rem;color:gray;font-weight:normal;'>{last_up}</span>" if last_up else btn_label
                        
                        if st.button(display_text, key=f"hist_{chat_id}", use_container_width=True):
                            st.session_state.active_chat = chat_id
                            st.rerun()
                            
                    with col_menu:
                        with st.popover("", use_container_width=True):
                            # Rename
                            new_name = st.text_input("Rename", value=meta["title"], key=f"ren_{chat_id}")
                            if st.button("Save Name", key=f"save_{chat_id}", type="primary", use_container_width=True):
                                if new_name.strip() and new_name.strip() != meta["title"]:
                                    st.session_state.story_metadata[chat_id]["title"] = new_name.strip()
                                    if st.session_state.active_chat == chat_id:
                                        st.session_state.story_title = new_name.strip()
                                    
                                    # Sync to DB
                                    db_id = meta.get("db_id")
                                    if db_id and getattr(st.session_state, "logged_in", False):
                                        from database.database import SessionLocal
                                        from services import story_service
                                        db = SessionLocal()
                                        story_service.update_story_content(
                                            db, db_id, st.session_state.auth_user_id,
                                            new_name.strip(),
                                            "\\n\\n".join([st.session_state.chapters.get(c, "") for c in st.session_state.chapter_order])
                                        )
                                        db.close()
                                    st.rerun()
                                    
                            # Pin / Unpin
                            pin_label = "Unpin Chat" if meta["pinned"] else "📌 Pin Chat"
                            if st.button(pin_label, key=f"pin_{chat_id}", use_container_width=True):
                                st.session_state.story_metadata[chat_id]["pinned"] = not meta["pinned"]
                                st.rerun()
                                
                            # Delete
                            if len(st.session_state.chats) > 1:
                                if st.button("🗑️ Delete", key=f"del_{chat_id}", use_container_width=True):
                                    st.session_state.chats.pop(chat_id, None)
                                    st.session_state.story_metadata.pop(chat_id, None)
                                    if st.session_state.active_chat == chat_id:
                                        st.session_state.active_chat = list(st.session_state.chats.keys())[-1]
                                    st.rerun()

                # Render Pinned section if needed
                if pinned_chats:
                    st.markdown('<div style="font-size:0.7rem; color:var(--accent); font-weight:bold; letter-spacing:0.05em; margin-bottom:0.2rem;">📌 PINNED</div>', unsafe_allow_html=True)
                    for chat_id in pinned_chats:
                        render_history_row(chat_id)
                    st.markdown('<hr style="margin: 0.5rem 0; opacity: 0.2;" />', unsafe_allow_html=True)
                
                # Render standard recent stories
                for chat_id in unpinned_chats:
                    render_history_row(chat_id)

        # ── Tags ──
        st.markdown('<div class="section-lbl">🏷 Tags</div>', unsafe_allow_html=True)
        active_story = st.session_state.active_chat
        if "story_tags" not in st.session_state:
            st.session_state.story_tags = {}
        current_tags = st.session_state.story_tags.get(active_story, [])

        # Show existing tags
        if current_tags:
            tags_html = " ".join(
                f'<span class="story-tag">{t}</span>' for t in current_tags
            )
            st.markdown(f'<div class="tags-container">{tags_html}</div>', unsafe_allow_html=True)

        # Add tag input
        new_tag = st.text_input(
            "Add Tag",
            placeholder="Add tag (press Enter)…",
            label_visibility="collapsed",
            key=f"tag_input_{active_story}",
        )
        if new_tag and new_tag.strip():
            tag_clean = new_tag.strip().lower()
            if tag_clean not in current_tags:
                updated = current_tags + [tag_clean]
                st.session_state.story_tags[active_story] = updated
                st.rerun()

        st.divider()

        # ── Ollama Status ──
        online, available = check_ollama()
        dot_class   = "online" if online else "offline"
        status_text = f"Ollama {'online' if online else 'offline'}"
        st.markdown(f"""
        <div style='text-align:center;margin:0.3rem 0 0.6rem;font-size:0.78rem;color:var(--muted);'>
            <span class='status-dot {dot_class}'></span>{status_text}
            {f"· {len(available)} model(s)" if online else ""}
        </div>
        """, unsafe_allow_html=True)

        if not online:
            st.warning("Start Ollama: `ollama serve`", icon="⚠️")

        st.divider()

        # ── AI Model Settings ──
        st.markdown('<div class="section-lbl">🤖 AI Model Settings</div>', unsafe_allow_html=True)
        model_options = sorted(set(MODELS) | set(available)) if available else MODELS
        default_idx   = model_options.index("llama3:latest") if "llama3:latest" in model_options else 0
        st.session_state.model = st.selectbox("Model", model_options, index=default_idx,
            help="llama3 is the default.")
        st.markdown(f"""
        <div style='margin:-6px 0 6px;'>
            <span class='model-badge'>⚙ {st.session_state.model} · local</span>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.temperature = st.slider(
            "Creativity Level", 0.0, 1.0,
            value=st.session_state.temperature, step=0.05, format="%.2f",
        )
        temp_label = (
            "🧊 Logical & controlled" if st.session_state.temperature < 0.3 else
            "⚖️ Balanced"             if st.session_state.temperature < 0.7 else
            "🔥 Highly creative"
        )
        st.caption(temp_label)

        st.session_state.length_mode = st.selectbox(
            "Response Length",
            ["Short", "Medium", "Long", "Chapter Mode"],
            index=["Short","Medium","Long","Chapter Mode"].index(st.session_state.length_mode),
        )

        st.divider()

        # ── Story Customization ──
        st.markdown('<div class="section-lbl">🎨 Story Customization</div>', unsafe_allow_html=True)
        st.session_state.genre = st.selectbox("Genre", GENRES,
            index=GENRES.index(st.session_state.genre))
        st.session_state.tone  = st.selectbox("Tone",  TONES,
            index=TONES.index(st.session_state.tone))
        st.session_state.writing_style = st.selectbox("Writing Style", STYLES,
            index=STYLES.index(st.session_state.writing_style))

        st.divider()

        # ── Chat Behavior ──
        st.markdown('<div class="section-lbl">⚙ Chat Behavior</div>', unsafe_allow_html=True)
        st.session_state.response_mode = st.radio(
            "Response Mode",
            ["Quick replies", "Detailed narration"],
            index=["Quick replies","Detailed narration"].index(st.session_state.response_mode),
            horizontal=True,
        )
        st.session_state.memory_mode = st.selectbox(
            "Memory Mode",
            ["Session only", "Persistent (coming soon)"],
            index=0,
        )
        st.session_state.auto_continue = st.toggle(
            "Auto-Continue Story",
            value=st.session_state.auto_continue,
        )

        st.divider()

        # ── UI Settings ──
        st.markdown('<div class="section-lbl">🖌 UI Settings</div>', unsafe_allow_html=True)
        new_theme = st.selectbox("Theme", ["Dark","Light","Custom"],
            index=["Dark","Light","Custom"].index(st.session_state.ui_theme))
        if new_theme != st.session_state.ui_theme:
            st.session_state.ui_theme = new_theme
            st.rerun()

        new_fs = st.slider("Font Size", 12, 20, st.session_state.font_size)
        if new_fs != st.session_state.font_size:
            st.session_state.font_size = new_fs
            st.rerun()

        new_bs = st.selectbox("Bubble Style", ["Glass style","Rounded","Minimal"],
            index=["Glass style","Rounded","Minimal"].index(st.session_state.bubble_style))
        if new_bs != st.session_state.bubble_style:
            st.session_state.bubble_style = new_bs
            st.rerun()

        st.divider()

        # ── Quick Starters ──
        st.markdown('<div class="section-lbl">⚡ Quick Starters</div>', unsafe_allow_html=True)
        for s in QUICK_STARTERS:
            if st.button(s[:35] + "…" if len(s) > 35 else s, key=f"st_{s}", use_container_width=True):
                add_message("user", s)
                h = get_flat_history()
                with st.spinner(""):
                    reply = call_ollama(h)
                add_message("assistant", reply)
                st.rerun()

        st.divider()

        # ── Future Features ──
        #st.markdown('<div class="section-lbl">🔮 Future Features</div>', unsafe_allow_html=True)
      #  st.session_state.voice_input_enabled = st.toggle(
       #     "🎙 Voice Input", value=False, disabled=True,
        #    help="Coming soon: streamlit-webrtc integration"
        #)
        #st.session_state.tts_enabled = st.toggle(
         #   "🔊 Text-to-Speech", value=False, disabled=True,
          #  help="Coming soon: pyttsx3 / coqui TTS integration"
        #)
