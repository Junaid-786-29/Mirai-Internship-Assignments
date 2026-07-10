
"""
Prompt Builder Module for Yapper Studio
Constructs prompts for Gemini using selected personality.
"""

from typing import List, Dict
from personalities.predefined import PREDEFINED_PERSONALITIES


def build_final_prompt(
    personality_name: str,
    user_message: str,
    conversation_history: List[Dict[str, str]]
) -> str:
    """
    Build the final prompt for Gemini using the selected personality, user message, and conversation history.
    Returns the constructed prompt.
    """
    # Get personality data
    personality = PREDEFINED_PERSONALITIES.get(personality_name, PREDEFINED_PERSONALITIES["Professor"])
    system_prompt = personality["system_prompt"]

    # Build conversation context
    conversation_context = "\n".join([
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in conversation_history
    ])

    # Final prompt
    final_prompt = f"""{system_prompt}

--- Conversation History:
{conversation_context}

--- Current User Message:
{user_message}

--- Please respond in the style of {personality_name}."""

    return final_prompt


def get_personality_system_prompt(personality_name: str) -> str:
    """Get just the system prompt for a given personality."""
    personality = PREDEFINED_PERSONALITIES.get(personality_name, PREDEFINED_PERSONALITIES["Professor"])
    return personality["system_prompt"]

