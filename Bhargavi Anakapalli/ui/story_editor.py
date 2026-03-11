import streamlit as st
from core.ollama import call_ollama
from core.chat_utils import add_message, get_flat_history
from core.export_utils import create_pdf_bytes, create_docx_bytes
from database.database import SessionLocal
from services import story_service


def _get_chapters():
    return st.session_state.get("chapter_order", ["Chapter 1"])


def _get_chapter_content():
    return st.session_state.chapters.get(st.session_state.active_chapter, "")


def render_story_editor():
    """Render the center story editor with title, chapter nav, and editor area."""

    # ── Story Title ──
    col_title, col_spacer = st.columns([4, 1])
    with col_title:
        new_title = st.text_input(
            "Story Title",
            value=st.session_state.story_title,
            placeholder="Story Title…",
            label_visibility="collapsed",
            key="story_title_input",
        )
        if new_title != st.session_state.story_title:
            st.session_state.story_title = new_title
            story_id = st.session_state.get("active_story_id")
            if story_id and getattr(st.session_state, "logged_in", False):
                db = SessionLocal()
                user_id = getattr(st.session_state, "auth_user_id", None)
                if user_id:
                    story_service.update_story_content(
                        db, story_id, user_id,
                        new_title,
                        "\\n\\n".join([st.session_state.chapters.get(c, "") for c in st.session_state.chapter_order])
                    )
                db.close()
                st.session_state.story_metadata[st.session_state.active_chat]["title"] = new_title

    # ── Chapter Navigation Bar ──
    chapters = _get_chapters()
    st.markdown('<div class="chapter-nav">', unsafe_allow_html=True)

    # Build chapter buttons inline
    ch_cols = st.columns(len(chapters) + 1)
    for i, ch_name in enumerate(chapters):
        with ch_cols[i]:
            is_active_ch = ch_name == st.session_state.active_chapter
            btn_type = "primary" if is_active_ch else "secondary"
            short_label = f"Ch{i+1}"
            if st.button(short_label, key=f"ch_nav_{i}", help=ch_name, type=btn_type, use_container_width=True):
                st.session_state.active_chapter = ch_name
                st.rerun()

    with ch_cols[-1]:
        if st.button("＋ Chapter", key="add_chapter_btn", use_container_width=True):
            st.session_state.chapter_counter += 1
            new_ch = f"Chapter {st.session_state.chapter_counter}"
            st.session_state.chapters[new_ch] = ""
            st.session_state.chapter_order.append(new_ch)
            st.session_state.active_chapter = new_ch
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Active Chapter Label ──
    st.markdown(
        f'<div class="chapter-label">✍ {st.session_state.active_chapter}</div>',
        unsafe_allow_html=True,
    )

    # ── Main Story Editor ──
    ch = st.session_state.active_chapter
    
    if "editor_sync_key" not in st.session_state:
        st.session_state.editor_sync_key = 0
        
    widget_key = f"editor_{ch}_{st.session_state.editor_sync_key}"

    def _sync_editor():
        if widget_key in st.session_state:
            st.session_state.chapters[ch] = st.session_state[widget_key]
            
            # --- DB Update ---
            if getattr(st.session_state, "logged_in", False):
                db = SessionLocal()
                user_id = getattr(st.session_state, "auth_user_id", None)
                story_title = st.session_state.story_title
                full_content = "\\n\\n".join([st.session_state.chapters.get(c, "") for c in st.session_state.chapter_order])
                
                story_id = st.session_state.get("active_story_id")
                if user_id:
                    if not story_id:
                        story = story_service.create_story(db, user_id, story_title, full_content)
                        st.session_state.active_story_id = story.id
                    else:
                        story_service.update_story_content(db, story_id, user_id, story_title, full_content)
                        story_service.save_story_version(db, story_id, full_content)
                db.close()

    st.text_area(
        "Story Chapter Editor",
        value=st.session_state.chapters.get(ch, ""),
        height=420,
        placeholder="Begin your story here… write scenes, paragraphs, and let the narrative flow.",
        label_visibility="collapsed",
        key=widget_key,
        on_change=_sync_editor
    )
    
    updated_content = st.session_state.chapters.get(ch, "")

    # ── Word Count Stats ──
    words = len(updated_content.split()) if updated_content.strip() else 0
    reading_mins = max(1, round(words / 200))
    st.markdown(
        f'<div class="editor-stats">'
        f'<span>📝 {words} words</span>'
        f'<span>⏱ ~{reading_mins} min read</span>'
        f'<span>📖 {st.session_state.active_chapter}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Bottom Story Controls ──
    bc1, bc2, bc3, bc4 = st.columns(4)
    
    # Determine if there is any exportable text across all chapters
    story_is_empty = True
    for c in st.session_state.chapter_order:
        if st.session_state.chapters.get(c, "").strip():
            story_is_empty = False
            break

    with bc1:
        try:
            pdf_bytes = create_pdf_bytes(st.session_state.story_title, st.session_state.chapter_order, st.session_state.chapters)
            st.download_button(
                "📄 Export PDF",
                data=pdf_bytes,
                file_name=f"{st.session_state.story_title.replace(' ','_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Export story as PDF document",
            )
        except Exception as e:
            st.button("📄 Export PDF", disabled=True, use_container_width=True, help="Error generating PDF")

    with bc2:
        try:
            docx_bytes = create_docx_bytes(st.session_state.story_title, st.session_state.chapter_order, st.session_state.chapters)
            st.download_button(
                "📝 Export DOCX",
                data=docx_bytes,
                file_name=f"{st.session_state.story_title.replace(' ','_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                help="Export story as Word document",
            )
        except Exception as e:
            st.button("📝 Export DOCX", disabled=True, use_container_width=True, help="Error generating DOCX")

    with bc3:
        if st.button("✨ Format Story", key="format_story_btn", use_container_width=True):
            raw = _get_chapter_content()
            if raw.strip():
                with st.spinner("Formatting…"):
                    formatted = call_ollama(
                        [{"role": "user", "content": raw}],
                        "Format and polish this story passage. Fix punctuation, paragraph breaks, and improve prose flow. Return only the improved text."
                    )
                if not formatted.startswith("⚠️"):
                    ch = st.session_state.active_chapter
                    st.session_state.chapters[ch] = formatted
                    st.session_state.editor_sync_key += 1
                    st.rerun()

    with bc4:
        if st.button("🗑 Clear Chat", key="clear_chat_btn", use_container_width=True, type="primary"):
            st.session_state.chats[st.session_state.active_chat] = []
            st.session_state.last_ai_suggestion = ""
            st.rerun()


def _build_full_story() -> str:
    lines = [f"# {st.session_state.story_title}\n"]
    for ch in st.session_state.chapter_order:
        content = st.session_state.chapters.get(ch, "")
        if content.strip():
            lines.append(f"\n## {ch}\n\n{content}")
    return "\n".join(lines) if len(lines) > 1 else "No story content yet."
