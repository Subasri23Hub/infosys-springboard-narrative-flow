import streamlit as st
import ollama
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NarrativeFlow",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "genre" not in st.session_state:
    st.session_state.genre = "Fantasy"

if "tone" not in st.session_state:
    st.session_state.tone = "Emotional"

# ─────────────────────────────────────────────
# OLLAMA STORY FUNCTION
# ─────────────────────────────────────────────
def generate_story(user_prompt, genre, tone, history):

    system_prompt = f"""
You are NarrativeFlow, an AI Story Co-Writer.

STRICT RULES:
- Only respond to storytelling and creative writing.
- If user asks about coding, science, math, general knowledge,
  politely refuse and redirect to storytelling.
- Always continue or assist with story writing.
- Genre: {genre}
- Tone: {tone}

If unrelated question:
"I am a storytelling assistant. Please ask something related to stories."
"""

    messages = [{"role": "system", "content": system_prompt}]

    for msg in history:
        messages.append(msg)

    messages.append({"role": "user", "content": user_prompt})

    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    return response["message"]["content"]

# ─────────────────────────────────────────────
# SIMPLE CLEAN CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Playfair+Display:wght@600&display=swap');

body {font-family: Inter;}
.main-title {
    font-family: 'Playfair Display';
    font-size: 46px;
    text-align: center;
    margin-top: 40px;
}
.subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 35px;
}
.welcome {
    text-align: center;
    color: #9ca3af;
    margin-top: 80px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🪶 NarrativeFlow")

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.current_chat = "New Chat"

    st.write("### 💬 Chat History")

    for chat_name in st.session_state.conversations.keys():
        if st.button(chat_name):
            st.session_state.current_chat = chat_name
            st.session_state.messages = st.session_state.conversations[chat_name]

    st.write("---")
    st.write("### ⚙️ Story Settings")

    st.session_state.genre = st.selectbox(
        "Genre",
        ["Fantasy","Sci-Fi","Romance","Mystery"]
    )

    st.session_state.tone = st.selectbox(
        "Tone",
        ["Emotional","Dark","Humorous"]
    )

# ─────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────
st.markdown("<div class='main-title'>NarrativeFlow</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Interactive Story Co-Writer</div>", unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("<div class='welcome'>Start writing your story…</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT DISPLAY
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────
if prompt := st.chat_input("Start writing your story…"):

    # Create new chat title
    if st.session_state.current_chat == "New Chat":
        title = prompt[:25] + "..."
        st.session_state.current_chat = title
        st.session_state.conversations[title] = []

    # Save user message
    st.session_state.messages.append({"role":"user","content":prompt})

    # REAL AI RESPONSE
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("✍️ Writing...")
        
        response = generate_story(
            prompt,
            st.session_state.genre,
            st.session_state.tone,
            st.session_state.messages
        )

        placeholder.markdown(response)

        st.session_state.messages.append(
            {"role":"assistant","content":response}
        )

    # Save conversation
    st.session_state.conversations[st.session_state.current_chat] = st.session_state.messages
    st.rerun()