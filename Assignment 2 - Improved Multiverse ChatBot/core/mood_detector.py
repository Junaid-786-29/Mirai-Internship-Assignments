
"""
Mood Detector Module for Yapper Studio
Lightweight keyword-based mood detection with personality suggestions.
"""

from typing import Dict, List, Literal
from personalities.custom_manager import get_personality
import streamlit as st


# Define mood types
MoodType = Literal["Happy", "Sad", "Angry", "Stressed", "Curious", "Neutral"]
ConfidenceType = Literal["High", "Medium", "Low"]


class MoodResult(Dict):
    mood: MoodType
    emoji: str
    confidence: ConfidenceType


# Mood keywords (lowercase)
MOOD_KEYWORDS: Dict[MoodType, List[str]] = {
    "Happy": ["happy", "excited", "great", "awesome", "amazing", "finally", "won", "success", "love", "joy", "fantastic"],
    "Sad": ["sad", "cry", "failed", "depressed", "upset", "hurt", "lonely", "unhappy", "heartbroken", "miserable", "down"],
    "Angry": ["angry", "hate", "annoyed", "furious", "mad", "irritated", "frustrated", "enraged"],
    "Stressed": ["stress", "exam", "deadline", "pressure", "overwhelmed", "tired", "burnout", "anxious", "worry"],
    "Curious": ["how", "why", "what", "explain", "teach me", "learn", "curious", "tell me", "wonder", "interesting"]
}


# Mood to emoji mapping
MOOD_EMOJIS: Dict[MoodType, str] = {
    "Happy": "😊",
    "Sad": "😔",
    "Angry": "😡",
    "Stressed": "😰",
    "Curious": "🤔",
    "Neutral": "😐"
}


# Mood to personality suggestions mapping
MOOD_PERSONALITY_SUGGESTIONS: Dict[MoodType, List[str]] = {
    "Happy": ["Professor", "Best Friend", "Motivational Coach"],
    "Sad": ["Therapist", "Best Friend", "Motivational Coach"],
    "Angry": ["Therapist", "Best Friend", "Detective"],
    "Stressed": ["Therapist", "Python Mentor", "Best Friend"],
    "Curious": ["Professor", "Python Mentor", "Detective"],
    "Neutral": []
}


def detect_mood(user_message: str) -> MoodResult:
    """
    Detect mood from user's message using keyword matching.
    Returns MoodResult with mood, emoji, and confidence.
    """
    user_message_lower = user_message.lower()
    mood_scores: Dict[MoodType, int] = {
        "Happy": 0,
        "Sad": 0,
        "Angry": 0,
        "Stressed": 0,
        "Curious": 0
    }

    # Count keyword matches for each mood
    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            if keyword in user_message_lower:
                mood_scores[mood] += 1

    # Find mood with highest score
    max_score = max(mood_scores.values())
    if max_score == 0:
        # No mood detected → Neutral
        return {
            "mood": "Neutral",
            "emoji": MOOD_EMOJIS["Neutral"],
            "confidence": "Low"
        }

    # Get mood with highest score
    detected_mood: MoodType = max(mood_scores, key=lambda m: mood_scores[m])  # type: ignore

    # Calculate confidence
    if max_score >= 3:
        confidence = "High"
    elif max_score >= 2:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "mood": detected_mood,
        "emoji": MOOD_EMOJIS[detected_mood],
        "confidence": confidence
    }


def get_suggested_personalities(mood: MoodType) -> List[Dict[str, str]]:
    """
    Get suggested personalities for a detected mood, with emoji and name.
    Returns list of dicts with "name" and "emoji".
    """
    personality_names = MOOD_PERSONALITY_SUGGESTIONS.get(mood, [])
    suggestions = []
    for name in personality_names:
        personality = get_personality(name, st.session_state.custom_personalities)
        if personality:
            suggestions.append({
                "name": personality["name"],
                "emoji": personality["emoji"]
            })
    return suggestions

