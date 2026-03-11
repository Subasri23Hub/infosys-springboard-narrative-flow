# ui/right_panel.py — Fixed vertical icon sidebar (Navigation)
import streamlit as st

from config.settings import PAGES

# Icon mapping for each page
PAGE_ICONS = {
    "💬 Story Chat":   "💬",
    "🗺 World Builder": "🌍",
    "🔧 Writer Tools":  "✍",
    "✏️ Split Editor":  "📝",
}

# Tooltip labels
PAGE_LABELS = {
    "💬 Story Chat":   "Story Chat",
    "🗺 World Builder": "World Builder",
    "🔧 Writer Tools":  "Writer Tools",
    "✏️ Split Editor":  "Split Editor",
}


def render_icon_nav():
    """Render the icon nav buttons horizontally."""
    st.markdown('<div class="top-icon-nav">', unsafe_allow_html=True)
    
    # Create columns for each icon to sit side-by-side
    cols = st.columns(len(PAGES))
    
    for i, page in enumerate(PAGES):
        with cols[i]:
            icon = PAGE_ICONS.get(page, "📄")
            label = PAGE_LABELS.get(page, page)
            is_active = page == st.session_state.current_page

            btn_key = f"icon_nav_{label.replace(' ', '_')}"
            btn_type = "primary" if is_active else "secondary"

            if st.button(icon, key=btn_key, help=label, type=btn_type, use_container_width=True):
                st.session_state.current_page = page
                try:
                    from core.persistence import save_session
                    if st.session_state.get("auth_username"):
                        save_session(st.session_state.auth_username)
                except Exception:
                    pass
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)


def render_right_panel():
    """Legacy: Render the main content area with a fixed icon sidebar on the right.
    Returns the main_col for backwards compatibility."""
    main_col, icon_col = st.columns([20, 1])
    with icon_col:
        render_icon_nav()
    return main_col
