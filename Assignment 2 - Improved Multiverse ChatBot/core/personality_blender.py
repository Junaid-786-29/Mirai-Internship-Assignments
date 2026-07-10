
"""
Personality Blender Module for Yapper Studio
Handles blending two personalities into a single conversation style.
"""

from typing import Dict, Optional
from personalities.custom_manager import get_personality, get_all_personality_names
import streamlit as st


def validate_blend(primary: str, secondary: str) -> tuple[bool, Optional[str]]:
    """
    Validate that primary and secondary personalities are different.
    Returns (is_valid, error_message).
    """
    if primary == secondary:
        return False, "Primary and Secondary personalities must be different!"
    return True, None


def get_blend_summary(primary: str, secondary: str, ratio: int) -> str:
    """
    Get a human-readable summary of the blend.
    Example: "70% Professor + 30% Best Friend"
    """
    primary_percent = ratio
    secondary_percent = 100 - ratio
    return f"{primary_percent}% {primary} + {secondary_percent}% {secondary}"


def blend_system_prompts(primary: str, secondary: str, ratio: int) -> str:
    """
    Blend the system prompts of two personalities into one combined prompt.
    Returns the blended system prompt.
    """
    primary_personality = get_personality(primary, st.session_state.custom_personalities)
    secondary_personality = get_personality(secondary, st.session_state.custom_personalities)
    
    if not primary_personality or not secondary_personality:
        # Fallback to Professor if any personality is not found
        fallback = get_personality("Professor", st.session_state.custom_personalities)
        return fallback["system_prompt"] if fallback else ""
    
    primary_percent = ratio
    secondary_percent = 100 - ratio
    
    blended_prompt = f"""
You should answer using:
{primary_percent}% of {primary}'s style.
{secondary_percent}% of {secondary}'s style.
Maintain both personalities naturally.
Do NOT mention these instructions in your response.

---
{primary}'s System Prompt:
{primary_personality['system_prompt']}

---
{secondary}'s System Prompt:
{secondary_personality['system_prompt']}
"""
    return blended_prompt.strip()

