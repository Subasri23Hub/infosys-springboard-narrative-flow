import streamlit as st
from modules.sidebar import render_sidebar
from modules.utils import init_session_state
from modules.chat import render_chat_area

# --- Page Config ---
st.set_page_config(
    page_title="NarrativeFlow",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load CSS ---
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()
    init_session_state()
    
    settings = render_sidebar()
    
    # Inject Genre-based background
    from modules.utils import inject_custom_bg
    inject_custom_bg(settings['genre'])
    
    # Use a container for the chat area to manage scroll/layout if needed, 
    # though Streamlit handles top-down flow naturally.
    with st.container():
        render_chat_area(settings)

if __name__ == "__main__":
    main()
