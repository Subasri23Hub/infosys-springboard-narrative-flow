# ui/writer_tools.py — Writer Tools tab
import streamlit as st

from core.chat_utils import get_history, add_message, get_flat_history, all_ai_text, word_count, reading_time
from core.ollama import call_ollama


def render_writer_tools():
    st.markdown("#### 🔧 Writer Tools")

    ai_text = all_ai_text()
    wc      = word_count(ai_text)
    rt      = reading_time(wc)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Words",   wc)
    m2.metric("Reading Time",  f"~{rt} min")
    m3.metric("AI Passages",   sum(1 for m in get_history() if m["role"] == "assistant"))

    st.divider()

    # Chapter Builder
    st.markdown("#### 📚 Chapter Builder")
    chap_num     = st.number_input("Chapter #", 1, 50, st.session_state.chapter_count)
    chap_title   = st.text_input("Chapter Title (optional):")
    chap_premise = st.text_area("What happens in this chapter?", height=90)
    if st.button("✍ Write Chapter", use_container_width=True) and chap_premise:
        title_part = f" — {chap_title}" if chap_title else ""
        prompt = f"Write Chapter {chap_num}{title_part}. Events: {chap_premise}"
        prev = ai_text[-400:] if ai_text else ""
        if prev:
            prompt += f"\n[Story so far ends with: …{prev}]"
        add_message("user", prompt)
        h = get_flat_history()
        old_len = st.session_state.length_mode
        st.session_state.length_mode = "Chapter Mode"
        with st.spinner(f"Writing Chapter {chap_num}…"):
            reply = call_ollama(h)
        st.session_state.length_mode = old_len
        add_message("assistant", reply)
        st.session_state.chapter_count = chap_num + 1
        st.success(f"Chapter {chap_num} written! Check Story Chat.")

    st.divider()

    # Paragraph Rewriter
    st.markdown("#### 🔄 Paragraph Rewriter")
    para  = st.text_area("Paste paragraph to rewrite:", height=100)
    instr = st.text_input("How to rewrite it:", placeholder="e.g., make it more poetic, add suspense, shorten it…")
    if st.button("🔄 Rewrite") and para and instr:
        prompt = f"Rewrite this paragraph — {instr}:\n\n{para}"
        h = [{"role": "user", "content": prompt}]
        with st.spinner("Rewriting…"):
            rewritten = call_ollama(h, instr)
        st.markdown(f"""
        <div class="editor-panel" style="min-height:auto;">
            {rewritten.replace(chr(10),"<br>")}
        </div>
        """, unsafe_allow_html=True)
        st.download_button("⬇ Save rewritten paragraph", data=rewritten, file_name="rewrite.txt", mime="text/plain")

    st.divider()

    # Export
    st.markdown("#### 📤 Export")
    if ai_text:
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "📄 Export Story (.txt)", data=ai_text,
                file_name=f"{st.session_state.active_chat.replace(' ','_')}_story.txt",
                mime="text/plain", use_container_width=True,
            )
        with dl2:
            full = "\n\n".join(
                f"[{m['role'].upper()}] {m['ts']}\n{m['content']}" for m in get_history()
            )
            st.download_button(
                "📋 Export Full Session (.txt)", data=full,
                file_name=f"{st.session_state.active_chat.replace(' ','_')}_session.txt",
                mime="text/plain", use_container_width=True,
            )
        st.markdown("**Preview (copy manually):**")
        st.code(ai_text[:1000] + ("…" if len(ai_text) > 1000 else ""), language=None)
    else:
        st.info("No story generated yet. Start in Story Chat.")

    st.divider()

    st.markdown("#### 🔮 Future Feature Stubs")
    with st.expander("Architecture Placeholders"):
        st.markdown("""
**Voice Input** → `streamlit-webrtc` + `whisper` transcription  
**Text-to-Speech** → `pyttsx3` or `coqui-ai/TTS`  
**PDF Export** → `reportlab` or `fpdf2`  
**Story Save/Load** → `sqlite3` or JSON file in `./saves/`
        """)
