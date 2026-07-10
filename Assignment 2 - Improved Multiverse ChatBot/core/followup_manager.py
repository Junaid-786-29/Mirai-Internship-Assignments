
"""
Follow-Up Manager Module for Yapper Studio
Handles generation of follow-up prompt actions for AI responses.
"""
from typing import Dict, List, Optional, Tuple


# Follow-up actions dictionary (icon: (name, prompt template))
FOLLOWUP_ACTIONS: Dict[str, Tuple[str, str]] = {
    "📖": (
        "Explain Simpler",
        "Explain your previous answer in simple language suitable for a beginner."
    ),
    "📝": (
        "Summarize",
        "Summarize your previous response into concise bullet points."
    ),
    "💡": (
        "Give Example",
        "Provide practical examples related to your previous answer."
    ),
    "➡": (
        "Continue",
        "Continue your previous response without repeating yourself."
    ),
    "🎯": (
        "Give Practical Steps",
        "Turn your previous answer into actionable step-by-step instructions."
    ),
    "⚔": (
        "Challenge Me",
        "Ask me questions or give me exercises to test my understanding of your previous explanation."
    ),
    "😂": (
        "Make It Funny",
        "Explain the same concept with humor while keeping the information accurate."
    ),
    "🔍": (
        "Explain In Detail",
        "Expand your previous answer with more technical depth and additional information."
    ),
    "❓": (
        "Ask Me Questions",
        "Act as a tutor and ask me questions based on your previous response."
    )
}


def get_followup_actions() -> List[Tuple[str, str, str]]:
    """
    Get all follow-up actions as list of tuples (icon, name, prompt template).

    Returns:
        List of tuples (icon, name, prompt template).
    """
    return [
        (icon, name, template) for icon, (name, template) in FOLLOWUP_ACTIONS.items()
    ]


def validate_context(
    last_user_message: Optional[str],
    last_assistant_message: Optional[str]
) -> bool:
    """
    Validate that required context exists for generating follow-up prompts.

    Returns:
        True if both last_user_message and last_assistant_message are not None/empty, else False.
    """
    return bool(last_user_message) and bool(last_assistant_message)


def build_context(
    last_user_message: Optional[str],
    last_assistant_message: Optional[str]
) -> Dict[str, Optional[str]]:
    """
    Build context dictionary for follow-up prompt generation.

    Returns:
        Dictionary with keys 'last_user_message' and 'last_assistant_message'.
    """
    return {
        "last_user_message": last_user_message,
        "last_assistant_message": last_assistant_message
    }


def generate_followup_prompt(
    action_icon: str,
    last_user_message: Optional[str],
    last_assistant_message: Optional[str]
) -> Optional[str]:
    """
    Generate complete follow-up prompt for selected action.

    Args:
        action_icon: Icon of the follow-up action (from FOLLOWUP_ACTIONS keys).
        last_user_message: Last message sent by user.
        last_assistant_message: Last response from AI assistant.

    Returns:
        Complete follow-up prompt string, or None if action is invalid or context is missing.
    """
    if not validate_context(last_user_message, last_assistant_message):
        return None
    if action_icon not in FOLLOWUP_ACTIONS:
        return None

    action_name, prompt_template = FOLLOWUP_ACTIONS[action_icon]
    context = build_context(last_user_message, last_assistant_message)

    # Build final prompt with context
    final_prompt = f"""{prompt_template}

---
Context:
Previous user question: {context['last_user_message']}
Your previous answer: {context['last_assistant_message']}"""
    return final_prompt


def execute_followup(
    action_icon: str,
    last_user_message: Optional[str],
    last_assistant_message: Optional[str]
) -> Optional[str]:
    """
    Execute a follow-up action and return the generated prompt.

    Wrapper for generate_followup_prompt() that returns the prompt to send to AI.

    Args:
        action_icon: Icon of the follow-up action.
        last_user_message: Last user message.
        last_assistant_message: Last assistant response.

    Returns:
        Generated prompt string or None if invalid.
    """
    return generate_followup_prompt(action_icon, last_user_message, last_assistant_message)
