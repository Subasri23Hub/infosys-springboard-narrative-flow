# ui/split_editor.py — Split Editor tab
import streamlit as st

from core.chat_utils import add_message
from core.ollama import call_ollama


def render_split_editor():
    st.markdown("#### ✏️ Split Editor — Write & Refine Side by Side")

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;'
                    'color:var(--muted);margin-bottom:4px;">📝 YOUR DRAFT</div>', unsafe_allow_html=True)
        draft = st.text_area(
            "draft",
            value=st.session_state.split_draft,
            height=400,
            placeholder="Write or paste your draft here…",
            label_visibility="collapsed",
            key="draft_area",
        )
        st.session_state.split_draft = draft

        split_action = st.selectbox("AI Action", [
            "Improve prose style",
            "Add vivid sensory detail",
            "Tighten and remove filler",
            "Rewrite in current tone & style",
            "Punch up the dialogue",
            "Fix pacing issues",
            "Suggest a natural continuation",
            "Convert to different perspective",
        ], key="split_act")

        run_ai = st.button("⚡ Run AI on Draft", use_container_width=True)

    with right_col:
        st.markdown('<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;'
                    'color:var(--muted);margin-bottom:4px;">🤖 AI SUGGESTIONS</div>', unsafe_allow_html=True)

        if run_ai and draft.strip():
            prompt = f"{split_action}:\n\n{draft}"
            h = [{"role": "user", "content": prompt}]
            with st.spinner(f"Running: {split_action}…"):
                suggestion = call_ollama(h, split_action)
            st.session_state["last_suggestion"] = suggestion

        sugg = st.session_state.get("last_suggestion", "")
        if sugg:
            st.markdown(f"""
            <div class="editor-panel">
                {sugg.replace(chr(10),"<br>")}
            </div>
            """, unsafe_allow_html=True)
            st.download_button("⬇ Download AI Version", data=sugg,
                               file_name="ai_suggestion.txt", mime="text/plain")
            if st.button("➕ Send AI version to Chat"):
                add_message("assistant", sugg)
                st.success("Added to story chat!")
        else:
            st.markdown("""
            <div class="editor-panel" style="display:flex;align-items:center;justify-content:center;min-height:380px;">
                <div style='text-align:center;color:var(--muted);'>
                    <div style='font-size:1.8rem;margin-bottom:6px;'>🪄</div>
                    <div>AI suggestions appear here</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
