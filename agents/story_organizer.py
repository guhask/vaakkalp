"""
VaakKalp - Story Organizer Agent
Transforms raw transcripts into structured, thematic digital memoir chapters.
Demonstrates: Long-context window management (Day 3), JSON structured output.
"""

import json

# Tool functions are defined as plain Python — importable without ADK
MEMOIR_CHAPTERS = [
    {"id": "childhood",     "title": "Roots & Childhood",       "description": "Early life, family, birthplace, childhood memories"},
    {"id": "livelihood",    "title": "Work & Craft",             "description": "Livelihood, traditional skills, farming, fishing, weaving"},
    {"id": "culture",       "title": "Festivals & Traditions",   "description": "Festivals, rituals, ceremonies, music, proverbs"},
    {"id": "history",       "title": "Living Through History",   "description": "Major historical events, community changes, migrations"},
    {"id": "relationships", "title": "People & Bonds",           "description": "Family, elders, mentors, community figures"},
    {"id": "philosophy",    "title": "Wisdom & Legacy",          "description": "Life lessons, values, advice for future generations"},
]


def get_memoir_structure() -> dict:
    """Returns the standard 6-chapter memoir structure."""
    return {
        "chapters": MEMOIR_CHAPTERS,
        "metadata_schema": {
            "speaker_name": "string",
            "language": "string",
            "region": "string",
            "approximate_birth_year": "int or null",
            "session_count": "int",
            "total_words": "int",
            "themes": "list of strings",
            "unique_cultural_terms": "list of strings",
            "significance_score": "float 0-1",
        },
    }


def calculate_significance_score(
    speaker_age: int,
    language_speaker_count: int,
    unique_terms_count: int,
) -> float:
    """Calculates a preservation significance score (0-1). Higher = more urgent."""
    age_score = min(speaker_age / 100, 1.0) if speaker_age else 0.5
    language_score = 1.0 - min(language_speaker_count / 100000, 1.0)
    term_score = min(unique_terms_count / 50, 1.0)
    return round((age_score * 0.4 + language_score * 0.4 + term_score * 0.2), 3)


# ADK Agent definition — only loaded when google-adk is installed
try:
    from google.adk.agents import Agent
    from google.adk.tools import FunctionTool

    story_organizer_agent = Agent(
        name="story_organizer",
        model="gemini-2.5-flash-lite",
        description="Structures oral history transcripts into thematic memoir chapters.",
        instruction="""
You are VaakKalp's Story Organizer. Transform enriched oral history transcripts into
structured 6-chapter digital memoirs. Call get_memoir_structure() first to get the schema,
then organize passages into chapters. Call calculate_significance_score() with speaker age,
language speaker count, and unique terms. NEVER paraphrase — preserve exact words spoken.
Return valid JSON matching the memoir schema.
""",
        tools=[FunctionTool(get_memoir_structure), FunctionTool(calculate_significance_score)],
    )
except ImportError:
    story_organizer_agent = None  # type: ignore
