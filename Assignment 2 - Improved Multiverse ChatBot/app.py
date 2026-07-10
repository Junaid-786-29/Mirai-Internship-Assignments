
"""
Main Application Entry Point for Yapper Studio - Clean, Minimal Design
"""

import streamlit as st
from components.sidebar import render_sidebar
from components.header import render_header
from components.chat import render_chat
from core.gemini_client import load_api_key


def load_css() -> None:
    """Load custom CSS from styles/main.css."""
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_session_state() -> None:
    """Initialize all required session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_personality" not in st.session_state:
        st.session_state.selected_personality = None
    if "temperature" not in st.session_state:
        st.session_state.temperature = 1.0
    if "blend_mode" not in st.session_state:
        st.session_state.blend_mode = False
    if "compare_mode" not in st.session_state:
        st.session_state.compare_mode = False
    if "compare_personalities" not in st.session_state:
        st.session_state.compare_personalities = []
    if "last_comparison" not in st.session_state:
        st.session_state.last_comparison = None
    if "favorite_replies" not in st.session_state:
        st.session_state.favorite_replies = []
    if "custom_personalities" not in st.session_state:
        st.session_state.custom_personalities = {}
    if "last_user_message" not in st.session_state:
        st.session_state.last_user_message = None
    if "last_assistant_message" not in st.session_state:
        st.session_state.last_assistant_message = None
    if "last_followup_action" not in st.session_state:
        st.session_state.last_followup_action = None


def check_api_key() -> None:
    """Check if API key is present and show warning if not."""
    if not load_api_key():
        st.warning(
            "Please set your GEMINI_API_KEY in the .env file. "
            "Copy .env.example to .env and add your key from Google AI Studio."
        )


def main() -> None:
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Yapper Studio",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load custom CSS
    load_css()

    # Initialize session state
    init_session_state()

    # Check for API key
    check_api_key()

    # Render components
    render_sidebar()
    render_header()
    render_chat()


if __name__ == "__main__":
    main()

