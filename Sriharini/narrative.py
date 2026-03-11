import streamlit as st
import uuid
import requests

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Narrative Flow Co-Writer",
    page_icon="✨📖",
    layout="wide"
)

# ---------------------------
# STORY CONTENT VALIDATION
# ---------------------------
def is_story_related(text):
    if len(text.split()) < 4:
        return False

    non_story_keywords = [
        "code", "python", "java", "html", "css",
        "math", "equation", "install", "error",
        "definition", "meaning", "who is", "what is"
    ]

    text_lower = text.lower()

    for word in non_story_keywords:
        if word in text_lower:
            return False

    return True


# ---------------------------
# CONTENT RESTRICTION FILTER (NEW)
# ---------------------------
def check_restricted_content(text):

    restricted_keywords = [
        "politics", "election", "government", "political party",
        "kill", "murder", "suicide", "violence", "harm",
        "hack", "hacking", "cyber attack", "bypass security",
        "password cracking", "malware", "phishing",
        "fraud", "steal", "illegal activity"
    ]

    text_lower = text.lower()

    for word in restricted_keywords:
        if word in text_lower:
            return False

    return True


# ---------------------------
# Ollama Backend Function
# ---------------------------
def generate_story_with_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "⚠️ Error connecting to Ollama."
    except:
        return "⚠️ Ollama server not running."


# ---------------------------
# Session Setup
# ---------------------------
if "all_chats" not in st.session_state:
    st.session_state.all_chats = []

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "previous_genre" not in st.session_state:
    st.session_state.previous_genre = None

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = "🪄Fantasy"

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.title("📖 Story Controls")

genre_options = ["🪄Fantasy", "👻Horror", "🚀Sci-Fi", "🔍Mystery"]

genre = st.sidebar.selectbox(
    "Genre",
    genre_options,
    index=genre_options.index(st.session_state.selected_genre)
)

st.session_state.selected_genre = genre

mode = st.sidebar.selectbox("Writing Mode", ["Continue", "Rewrite", "Enhance"])
tone = st.sidebar.selectbox("Tone", ["Dark", "Emotional", "Suspense", "Epic"])

# ---------------------------
# New Chat When Genre Changes
# ---------------------------
if st.session_state.previous_genre is None:
    st.session_state.previous_genre = genre

if st.session_state.previous_genre != genre:
    st.session_state.current_chat_id = None
    st.session_state.previous_genre = genre

active_genre = st.session_state.selected_genre

# ---------------------------
# Dynamic Gradient Background
# ---------------------------
if active_genre == "🚀Sci-Fi":
    background = "linear-gradient(135deg, #0f2027, #203a43, #2c5364, #00c6ff)"
    text_color = "white"

elif active_genre == "👻Horror":
    background = "linear-gradient(135deg, #000000, #1a0000, #400000, #660000)"
    text_color = "white"

elif active_genre == "🔍Mystery":
    background = "linear-gradient(135deg, #f8e6c1, #eacb9f, #d4a373, #b07d4f, #8b5e34)"
    text_color = "#3b1f0f"

elif active_genre == "🪄Fantasy":
    background = "linear-gradient(135deg, #ffd6e8, #ffc2dd, #ffb3d9, #e0bbff, #d5b6ff)"
    text_color = "#5a3e6b"

# ---------------------------
# Apply Animated Gradient Styling
# ---------------------------
st.markdown(f"""
<style>

@keyframes gradientMove {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.stApp {{
    background: {background};
    background-size: 300% 300%;
    animation: gradientMove 12s ease infinite;
    background-attachment: fixed;
    color: {text_color};
}}

.chat-box {{
    background: rgba(255,255,255,0.25);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

.stDownloadButton button {{
    color: white !important;
    font-weight: bold;
    border-radius: 8px;
}}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar Chat History
# ---------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📝 Chat History")

for chat in st.session_state.all_chats:
    label = f"{chat['genre']} ➜ {chat['title']}"
    if st.sidebar.button(label, key=chat["id"]):
        st.session_state.current_chat_id = chat["id"]
        st.session_state.selected_genre = chat["genre"]
        st.session_state.previous_genre = chat["genre"]
        st.rerun()

# ---------------------------
# Get Current Chat
# ---------------------------
current_chat = None
if st.session_state.current_chat_id:
    for chat in st.session_state.all_chats:
        if chat["id"] == st.session_state.current_chat_id:
            current_chat = chat
            break

# ---------------------------
# Title
# ---------------------------
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
<h1>✨📖 Narrative Flow Co-Writer</h1>
<p>Your co-writer in every chapter of creativity...</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Download Story
# ---------------------------
if current_chat and current_chat["messages"]:
    story_text = ""
    for msg in current_chat["messages"]:
        if msg["role"] == "bot":
            story_text += msg["content"] + "\n\n"

    if story_text.strip():
        st.download_button(
            label="📖 Download Story",
            data=story_text,
            file_name=f"{current_chat['genre']}_story.txt",
            mime="text/plain"
        )

# ---------------------------
# Show Messages
# ---------------------------
if current_chat:
    for msg in current_chat["messages"]:
        role = "You" if msg["role"] == "user" else "Story AI"
        st.markdown(
            f'<div class="chat-box"><b>{role}:</b><br>{msg["content"]}</div>',
            unsafe_allow_html=True
        )

# ---------------------------
# Chat Input
# ---------------------------
user_input = st.chat_input("Write your story idea here...")

if user_input:

    if not current_chat:
        new_chat = {
            "id": str(uuid.uuid4()),
            "genre": genre,
            "title": user_input[:30],
            "messages": []
        }
        st.session_state.all_chats.append(new_chat)
        st.session_state.current_chat_id = new_chat["id"]
        current_chat = new_chat

    current_chat["messages"].append({
        "role": "user",
        "content": user_input
    })

    full_prompt = f"""
You are a creative story writer.

Genre: {genre}
Tone: {tone}
Mode: {mode}

User Idea:
{user_input}

Write a story based on these settings.
"""

    # 🔒 VALIDATION + RESTRICTION
    if not is_story_related(user_input):
        reply = "⚠️ This app generates story-based content only. Please enter a valid story idea."

    elif not check_restricted_content(user_input):
        reply = "⚠️ This topic is restricted. can i expalin something else"

    else:
        with st.spinner("Thinking..."):
            reply = generate_story_with_ollama(full_prompt)

    current_chat["messages"].append({
        "role": "bot",
        "content": reply
    })

    st.rerun()
