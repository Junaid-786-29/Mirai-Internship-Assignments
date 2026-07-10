
"""Header component for Yapper Studio - Clean, Minimal Design"""

import streamlit as st


def render_header():
    """Render the main page header."""
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1>🤖 Yapper Studio</h1>
            <p style="font-size: 1.5rem; color: #6B7280; margin-bottom: 0.5rem;">
                One AI. Infinite Personalities.
            </p>
            <p style="color: #9CA3AF;">
                Choose a personality and start chatting with AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

