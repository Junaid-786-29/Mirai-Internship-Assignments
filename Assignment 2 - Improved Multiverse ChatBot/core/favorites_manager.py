
"""
Favorites Manager Module for Yapper Studio
Handles saving, deleting, searching, sorting, and exporting favorite replies.
"""
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FavoriteReply:
    id: str
    timestamp: str
    personality: str
    emoji: str
    question: str
    response: str


def _generate_unique_id() -> str:
    """Generate a unique ID using timestamp."""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def _get_current_timestamp() -> str:
    """Get current timestamp as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_favorite(
    favorites: List[Dict],
    personality: str,
    emoji: str,
    question: str,
    response: str
) -> tuple[List[Dict], str]:
    """
    Save a new favorite reply, checking for duplicates first.

    Returns:
        Tuple of (updated favorites list, status message)
    """
    # Check for duplicates
    for fav in favorites:
        if (
            fav["personality"] == personality
            and fav["question"] == question
            and fav["response"] == response
        ):
            return favorites, "This reply is already in Favorites!"
    
    # Create new favorite
    new_favorite = {
        "id": _generate_unique_id(),
        "timestamp": _get_current_timestamp(),
        "personality": personality,
        "emoji": emoji,
        "question": question,
        "response": response
    }
    
    favorites.append(new_favorite)
    return favorites, "Reply added to Favorites."


def delete_favorite(favorites: List[Dict], favorite_id: str) -> List[Dict]:
    """
    Delete a favorite reply by ID.

    Returns:
        Updated favorites list
    """
    return [fav for fav in favorites if fav["id"] != favorite_id]


def is_favorite(
    favorites: List[Dict],
    personality: str,
    question: str,
    response: str
) -> bool:
    """
    Check if a reply is already in favorites.
    """
    for fav in favorites:
        if (
            fav["personality"] == personality
            and fav["question"] == question
            and fav["response"] == response
        ):
            return True
    return False


def search_favorites(favorites: List[Dict], search_query: str) -> List[Dict]:
    """
    Filter favorites by search query (case-insensitive).
    Searches question, response, and personality name.
    """
    if not search_query:
        return favorites
    search_lower = search_query.lower()
    return [
        fav for fav in favorites
        if (search_lower in fav["question"].lower()
            or search_lower in fav["response"].lower()
            or search_lower in fav["personality"].lower())
    ]


def sort_favorites(favorites: List[Dict], sort_by: str) -> List[Dict]:
    """
    Sort favorites:
    - "newest": Newest first (default)
    - "oldest": Oldest first
    - "personality": Alphabetical by personality name
    """
    if sort_by == "newest":
        return sorted(favorites, key=lambda x: x["timestamp"], reverse=True)
    elif sort_by == "oldest":
        return sorted(favorites, key=lambda x: x["timestamp"])
    elif sort_by == "personality":
        return sorted(favorites, key=lambda x: x["personality"])
    else:
        return favorites


def export_favorites(favorites: List[Dict]) -> str:
    """
    Export all favorites as Markdown.
    """
    md_content = "# Favorite Replies\n\n"
    for fav in favorites:
        md_content += f"## {fav['emoji']} {fav['personality']}\n\n"
        md_content += f"### Question\n\n{fav['question']}\n\n"
        md_content += f"### Response\n\n{fav['response']}\n\n"
        md_content += f"### Saved at\n\n{fav['timestamp']}\n\n---\n\n"
    return md_content

