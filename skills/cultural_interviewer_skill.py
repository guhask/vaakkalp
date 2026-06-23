"""
VaakKalp - Cultural Interviewer Skill
A reusable ADK skill for conducting oral history interviews.
Demonstrates: Agent Skills (Day 3) — exportable via ADK CLI.

Export with: adk skill export cultural_interviewer
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class InterviewConfig:
    """Configuration for the Cultural Interviewer Skill."""
    community_context: str = "general"  # e.g., "tribal", "agrarian", "maritime", "urban"
    primary_language: str = "en"
    session_duration_mins: int = 45
    topics_to_cover: list[str] = field(default_factory=lambda: [
        "childhood", "livelihood", "culture", "history", "relationships", "philosophy"
    ])
    sensitive_topics_excluded: list[str] = field(default_factory=list)
    interviewer_name: str = "VaakKalp"


def build_cultural_interviewer_skill(config: InterviewConfig) -> Agent:
    """
    Factory function that builds a Cultural Interviewer Agent
    configured for a specific community context.

    Args:
        config: InterviewConfig with community-specific settings

    Returns:
        A configured ADK Agent ready for oral history interviews.
    """

    def get_community_opener(community: str, language: str) -> str:
        """Get a culturally appropriate session opener."""
        openers = {
            "tribal": (
                "Namaste. I am here to listen and learn from your experiences. "
                "Your stories and your community's wisdom are precious gifts. "
                "With your permission, I would love to hear about your life."
            ),
            "agrarian": (
                "Pranam. I come as a student, hoping to learn from your years of "
                "wisdom and hard work on the land. Your life's story carries knowledge "
                "that books cannot hold. May I listen?"
            ),
            "maritime": (
                "Greetings. The sea holds many stories, and so do those who have "
                "sailed it all their lives. I would be honored to hear about your "
                "journey — the tides, the catches, the people, the changes."
            ),
            "urban": (
                "Hello. A city is made of millions of individual stories — and yours "
                "is one of them. I am here to listen, to learn, and to ensure your "
                "experiences are remembered."
            ),
        }
        return openers.get(community, openers["urban"])

    def check_session_completeness(
        topics_covered: list[str],
        required_topics: list[str],
    ) -> dict:
        """Check which topics are covered and what remains."""
        covered = set(topics_covered)
        required = set(required_topics)
        missing = required - covered
        return {
            "covered": list(covered),
            "missing": list(missing),
            "completion_percent": round(len(covered) / max(len(required), 1) * 100, 1),
            "is_complete": len(missing) == 0,
        }

    opener_tool = FunctionTool(get_community_opener)
    completeness_tool = FunctionTool(check_session_completeness)

    skill_prompt = f"""
You are the VaakKalp Cultural Interviewer Skill, configured for: {config.community_context}
community context, interviewing in: {config.primary_language}.

SKILL PARAMETERS:
- Community context: {config.community_context}
- Session target: {config.session_duration_mins} minutes
- Topics to cover: {', '.join(config.topics_to_cover)}
- Excluded topics: {', '.join(config.sensitive_topics_excluded) or 'None'}

BEGIN SESSION:
1. Call get_community_opener("{config.community_context}", "{config.primary_language}")
   to open with culturally appropriate greeting.
2. Ask one question at a time. Never rush.
3. Probe interesting threads before moving to next topic.
4. Periodically call check_session_completeness() to track coverage.
5. When all topics covered or time limit approached, gracefully close the session.

SKILL CONTRACT (for external integrations):
- Input: user_message (str), session_state (dict)
- Output: next_question (str), updated_session_state (dict), topics_covered (list)
"""

    return Agent(
        name=f"cultural_interviewer_{config.community_context}",
        model="gemini-2.5-flash-lite",
        description=(
            f"Cultural Interviewer Skill for {config.community_context} community context. "
            "Conducts oral history interviews in a culturally sensitive manner. "
            "Exportable via ADK CLI for use in other preservation projects."
        ),
        instruction=skill_prompt,
        tools=[opener_tool, completeness_tool],
    )


# --------------------------------------------------------------------------
# Pre-built skill instances for common contexts
# --------------------------------------------------------------------------

tribal_interviewer = build_cultural_interviewer_skill(
    InterviewConfig(community_context="tribal", primary_language="hi")
)

agrarian_interviewer = build_cultural_interviewer_skill(
    InterviewConfig(community_context="agrarian", primary_language="mr")
)

maritime_interviewer = build_cultural_interviewer_skill(
    InterviewConfig(
        community_context="maritime",
        primary_language="ta",
        topics_to_cover=["childhood", "livelihood", "culture", "history", "philosophy"],
    )
)
