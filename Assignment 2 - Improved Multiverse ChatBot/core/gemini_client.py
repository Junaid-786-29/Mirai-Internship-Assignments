"""Gemini client for Yapper Studio.

Handles API initialization, streaming responses, and personality integration for
single and blended personalities.
"""

import os
from typing import Dict, Iterator, List

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from core.personality_blender import blend_system_prompts
from personalities.custom_manager import get_personality


# Configuration section
MODEL_NAME = "gemini-3.5-flash"
TEMPERATURE = 1.0
MAX_OUTPUT_TOKENS = 8192
SAFETY_SETTINGS = [
    types.SafetySetting(
        category=category,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    )
    for category in (
        types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    )
]


def load_api_key() -> str | None:
    """Load the Gemini API key from the environment or .env file."""
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def initialize_gemini() -> genai.Client:
    """Create an authenticated Google GenAI client."""
    api_key = load_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables or .env file")

    return genai.Client(api_key=api_key)


def _get_system_prompt(personality_name: str) -> str:
    """Return the active single or blended personality instruction."""
    if st.session_state.blend_mode:
        return blend_system_prompts(
            st.session_state.primary_personality,
            st.session_state.secondary_personality,
            st.session_state.blend_ratio,
        )

    personality = get_personality(personality_name, st.session_state.custom_personalities)
    if not personality:
        personality = get_personality("Professor", st.session_state.custom_personalities)
    return personality["system_prompt"]


def _build_history(messages: List[Dict[str, str]]) -> List[types.Content]:
    """Convert prior UI messages to Gemini chat history.

    The first stored message is Yapper Studio's greeting, so it is not sent to
    Gemini. The latest user message is sent separately as the streaming request.
    """
    history: List[types.Content] = []
    for message in messages[1:-1]:
        role = "user" if message["role"] == "user" else "model"
        history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=message["content"])],
            )
        )
    return history


def stream_response_with_personality(
    messages: List[Dict[str, str]], personality_name: str
) -> Iterator[str]:
    """Stream a Gemini response using the selected personality instruction."""
    if not messages or messages[-1]["role"] != "user":
        raise ValueError("A user message is required before requesting a response")

    client = initialize_gemini()
    config = types.GenerateContentConfig(
        system_instruction=_get_system_prompt(personality_name),
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        safety_settings=SAFETY_SETTINGS,
    )
    try:
        chat = client.chats.create(
            model=MODEL_NAME,
            config=config,
            history=_build_history(messages),
        )
        for chunk in chat.send_message_stream(messages[-1]["content"]):
            if chunk.text:
                yield chunk.text
    finally:
        client.close()
