
"""
Compare Engine Module for Yapper Studio
Handles all compare mode logic: validation, prompt building, response generation, export.
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from personalities.custom_manager import get_personality
from core.gemini_client import stream_response_with_personality


@dataclass
class ComparisonResult:
    personality_name: str
    personality_emoji: str
    response: Optional[str] = None
    error: Optional[str] = None


def validate_selection(selected_personalities: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate the compare mode personality selection.
    Returns (is_valid, error_message).
    """
    if len(selected_personalities) < 2:
        return False, "Please select at least 2 personalities to compare."
    if len(selected_personalities) > 4:
        return False, "You can select a maximum of 4 personalities to compare."
    return True, None


def export_comparison(question: str, results: List[ComparisonResult]) -> str:
    """
    Export a comparison as Markdown.
    """
    md_content = f"# Question\n\n{question}\n\n"
    for result in results:
        md_content += f"## {result.personality_emoji} {result.personality_name}\n\n"
        if result.error:
            md_content += f"Error: {result.error}\n\n"
        elif result.response:
            md_content += f"{result.response}\n\n"
    return md_content
