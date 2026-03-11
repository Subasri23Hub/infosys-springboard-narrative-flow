# ui/world_builder.py — World Builder tab
import streamlit as st

from core.chat_utils import add_message, get_flat_history
from core.ollama import call_ollama
from core.prompts import build_system_prompt
from config.settings import PERSONALITIES


def render_world_builder():
    st.markdown("#### 🗺 World & Character Builder")
    st.caption("Everything here is injected into every llama3 generation call.")

    ctx = st.session_state.story_context

    col_a, col_b = st.columns(2)
    with col_a:
        ctx["title"]     = st.text_input("Story Title",          value=ctx.get("title",""),     placeholder="Leave blank for untitled")
        ctx["char_name"] = st.text_input("Main Character Name",  value=ctx.get("char_name",""), placeholder="e.g., Elara Voss")
        ctx["perspective"] = st.selectbox(
            "Story Perspective",
            ["Third person","First person","Second person (experimental)"],
            index=["Third person","First person","Second person (experimental)"].index(ctx.get("perspective","Third person")),
        )
    with col_b:
        ctx["setting"] = st.text_area(
            "World / Setting Description", value=ctx.get("setting",""), height=110,
            placeholder="Describe the world, era, location, atmosphere…",
        )
        ctx["char_personality"] = st.multiselect(
            "Character Personality", PERSONALITIES,
            default=ctx.get("char_personality",["Brave"]),
        )

    st.session_state.story_context = ctx

    if st.button("✅ Save World Context", use_container_width=True):
        st.success("Context saved! All future llama3 calls will use this world.")

    with st.expander("👁 Preview: What llama3 receives as system prompt"):
        st.code(build_system_prompt(), language=None)

    st.divider()

    # AI Character Generator
    st.markdown("#### 🧬 AI Character Generator")
    char_concept = st.text_input("Describe a character concept:", placeholder="e.g., a weary detective haunted by one case")
    if st.button("🧬 Generate Character Profile") and char_concept:
        prompt = f"""Generate a detailed character profile for: {char_concept}

Format exactly as:
NAME: ...
AGE: ...
APPEARANCE: ...
PERSONALITY: ...
BACKSTORY: ...
GOAL: ...
FATAL FLAW: ...
DISTINCTIVE HABIT: ...
FIRST LINE OF DIALOGUE: "..."
"""
        h = [{"role": "user", "content": prompt}]
        with st.spinner("Generating character…"):
            profile = call_ollama(h, "Create a rich, vivid, three-dimensional character profile.")
        st.markdown(f"""
        <div class="editor-panel" style="min-height:auto;margin-top:0.75rem;">
            {profile.replace(chr(10),"<br>")}
        </div>
        """, unsafe_allow_html=True)
        st.download_button("⬇ Save Character", data=profile, file_name="character.txt", mime="text/plain")

    st.divider()

    # Outline Builder
    st.markdown("#### 📋 Outline Builder")
    new_beat = st.text_input("Add a story beat:", placeholder="e.g., Hero discovers the map is a lie")
    if st.button("Add Beat") and new_beat:
        st.session_state.outline.append(new_beat)
        st.rerun()

    if st.session_state.outline:
        for j, beat in enumerate(st.session_state.outline):
            bca, bcb, bcc = st.columns([6,1,1])
            with bca:
                st.markdown(f"**{j+1}.** {beat}")
            with bcb:
                if st.button("✍", key=f"wb_{j}", help="Write this beat"):
                    add_message("user", f"Write a scene for: {beat}")
                    h = get_flat_history()
                    with st.spinner("Writing scene…"):
                        reply = call_ollama(h)
                    add_message("assistant", reply)
            with bcc:
                if st.button("🗑", key=f"db_{j}"):
                    st.session_state.outline.pop(j)
                    st.rerun()

        if st.button("🚀 Generate Full Story from Outline"):
            outline_str = "\n".join(f"{i+1}. {b}" for i,b in enumerate(st.session_state.outline))
            add_message("user", f"Write a complete story following this outline:\n{outline_str}")
            h = get_flat_history()
            old_len = st.session_state.length_mode
            st.session_state.length_mode = "Chapter Mode"
            with st.spinner("Generating full story from outline…"):
                reply = call_ollama(h)
            st.session_state.length_mode = old_len
            add_message("assistant", reply)
            st.success("Story generated! Switch to Story Chat to read it.")
