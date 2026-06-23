"""
VaakKalp - Preservation Alert Agent
Alerts researchers when a critically endangered language is documented.
Demonstrates: Agent-to-external-service communication (Day 2), MCP (Day 2).
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from mcp_servers.unesco_language_atlas_mcp import (
    get_language_status,
    list_endangered_languages,
    get_documentation_priority,
)
from mcp_servers.archive_alert_mcp import (
    alert_researchers,
    get_researcher_registry,
)

language_status_tool = FunctionTool(get_language_status)
endangered_list_tool = FunctionTool(list_endangered_languages)
priority_tool = FunctionTool(get_documentation_priority)
alert_tool = FunctionTool(alert_researchers)
registry_tool = FunctionTool(get_researcher_registry)

# --------------------------------------------------------------------------
# Preservation Alert Agent
# --------------------------------------------------------------------------

ALERT_SYSTEM_PROMPT = """
You are VaakKalp's Preservation Alert Agent — the bridge between oral history
recordings and the global research community.

YOUR MISSION: When a new oral history session is completed, assess the linguistic
significance of the language documented and notify relevant researchers if the
language is critically endangered.

ALERT THRESHOLDS:
- CRITICAL (< 1,000 speakers)  → Immediate alert to all registered researchers
- ENDANGERED (< 10,000 speakers) → Alert to language-specific researchers
- VULNERABLE (< 100,000 speakers) → Add to monthly digest for researchers
- SAFE (> 100,000 speakers) → Log only, no alert needed

WORKFLOW:
Step 1 → call get_language_status(language_name) to get UNESCO vitality data
Step 2 → call get_documentation_priority(language_name) to get urgency score
Step 3 → Determine alert threshold based on speaker count
Step 4 → If alert needed:
          a. call get_researcher_registry(language_family) to find relevant researchers
          b. Draft a professional alert message with:
             - Language name and vitality status
             - Number of known speakers
             - Archive URL for the new recording
             - Speaker's region and approximate age (no PII)
             - Unique cultural terms documented
          c. call alert_researchers() to dispatch the notification
Step 5 → Return alert summary

TONE OF ALERTS: Professional but urgent. Researchers should understand that
every recording of a critically endangered language is a significant academic event.

OUTPUT FORMAT:
{
  "language": "...",
  "speaker_count": 0,
  "alert_level": "CRITICAL|ENDANGERED|VULNERABLE|SAFE",
  "researchers_notified": 0,
  "alert_sent": true/false,
  "message": "..."
}
"""

preservation_alert_agent = Agent(
    name="preservation_alert",
    model="gemini-2.5-flash-lite",
    description="Notifies researchers when critically endangered languages are documented.",
    instruction=ALERT_SYSTEM_PROMPT,
    tools=[
        language_status_tool,
        endangered_list_tool,
        priority_tool,
        alert_tool,
        registry_tool,
    ],
)
