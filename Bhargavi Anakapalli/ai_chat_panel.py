import streamlit as st
from core.ollama import call_ollama
from core.chat_utils import add_message, get_history, get_flat_history
from database.database import SessionLocal
from services import chat_service


def render_ai_chat_panel():
    """Render the right AI assistant chat panel."""

    # ── Top Navigation Icons ──
    from ui.right_panel import render_icon_nav
    render_icon_nav()

    # ── Header ──
    st.markdown("""
    <div class="ai-panel-header">
        <span class="ai-panel-icon">✍️</span>
        <span class="ai-panel-title">AI Assistant</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Ollama status dot ──
    from core.ollama import check_ollama
    online, _ = check_ollama()
    dot = "🟢" if online else "🔴"
    st.markdown(
        f'<div class="ai-status">{dot} {"Online · " + st.session_state.model if online else "Ollama offline"}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="ai-chat-messages">', unsafe_allow_html=True)

    # ── Chat History ──
    history = get_history()
    if not history:
        st.markdown("""
        <div class="ai-empty-state">
            <div style="font-size:2rem;margin-bottom:0.5rem;">✨</div>
            <div>Ask your AI co-writer anything.<br>Build characters, expand scenes, or continue the story.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, msg in enumerate(history):
            role = msg["role"]
            content = msg["content"]
            ts = msg.get("ts", "")
            if role == "user":
                st.markdown(f"""
                <div class="ai-msg-user">
                    <div class="ai-msg-bubble user">{content}</div>
                    <div class="ai-msg-meta">{ts}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # AI message — render content + action buttons
                st.markdown(f"""
                <div class="ai-msg-ai">
                    <div class="ai-avatar">✍️</div>
                    <div style="flex:1;min-width:0;">
                        <div class="ai-suggestion-card">{content}</div>
                        <div class="ai-msg-meta">{ts} · {st.session_state.model}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Action buttons for each AI message
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button("＋ Add", key=f"add_story_{i}", use_container_width=True, help="Add to Story"):
                        ch = st.session_state.active_chapter
                        current = st.session_state.chapters.get(ch, "")
                        separator = "\n\n" if current.strip() else ""
                        new_text = current + separator + content
                        
                        st.session_state.chapters[ch] = new_text
                        st.session_state.editor_sync_key = st.session_state.get("editor_sync_key", 0) + 1
                        
                        st.success("✅ Added to story!")
                        st.rerun()
                with btn_col2:
                    if st.button("↩ Rewrite", key=f"rewrite_{i}", use_container_width=True, help="Rewrite this"):
                        with st.spinner("Rewriting…"):
                            reply = call_ollama(
                                [{"role": "user", "content": content}],
                                "Rewrite this passage in a completely different style, keeping the same story ideas."
                            )
                        add_message("assistant", reply)
                        st.rerun()
                with btn_col3:
                    if st.button("⤢ Expand", key=f"expand_{i}", use_container_width=True, help="Expand this"):
                        with st.spinner("Expanding…"):
                            reply = call_ollama(
                                [{"role": "user", "content": content}],
                                "Expand this passage into a longer, more detailed and immersive version."
                            )
                        add_message("assistant", reply)
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Chat Input ──
    user_input = st.chat_input(
        f"Ask your co-writer… {st.session_state.model}",
        key="ai_panel_chat_input",
    )

    if user_input:
        add_message("user", user_input)
        h = get_flat_history()
        with st.spinner("Writing…"):
            reply = call_ollama(h)
        add_message("assistant", reply)
        # Store latest AI suggestion for quick access
        st.session_state.last_ai_suggestion = reply
        
        # --- DB Update ---
        if getattr(st.session_state, "logged_in", False) and getattr(st.session_state, "active_story_id", None):
            db = SessionLocal()
            chat_service.save_chat(db, st.session_state.active_story_id, "user", user_input)
            chat_service.save_chat(db, st.session_state.active_story_id, "assistant", reply)
            db.close()

        if st.session_state.auto_continue and not reply.startswith("⚠️"):
            h2 = get_flat_history()
            with st.spinner("Auto-continuing…"):
                continuation = call_ollama(h2, "Continue the story naturally from where it left off.")
            add_message("assistant", continuation)

        st.rerun()
