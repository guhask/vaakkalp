"""
VaakKalp - Transcription & Translation Agent
Detects language/dialect, transcribes audio, produces parallel translations.
Demonstrates: MCP tool use (Translation MCP), external API integration (Day 2).
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from mcp_servers.translation_mcp import (
    detect_language,
    translate_text,
    transliterate_to_script,
    get_low_resource_model,
)

# Wrap MCP functions as ADK tools
detect_language_tool = FunctionTool(detect_language)
translate_text_tool = FunctionTool(translate_text)
transliterate_tool = FunctionTool(transliterate_to_script)
low_resource_model_tool = FunctionTool(get_low_resource_model)

# --------------------------------------------------------------------------
# Transcription Agent
# --------------------------------------------------------------------------

TRANSCRIPTION_SYSTEM_PROMPT = """
You are VaakKalp's Transcription & Translation Agent.

YOUR MISSION: Take text (from voice or typed input) and produce:
1. A clean, faithful transcription in the original language/script
2. An English translation that preserves cultural nuance
3. A translation in the dominant regional language (Hindi for North India,
   Marathi for Maharashtra, Tamil for Tamil Nadu, etc.)

WORKFLOW:
Step 1 → detect_language() — identify the language code and any dialect hints
Step 2 → If language is low-resource (<100k speakers), call get_low_resource_model()
          to use the specialized Bhashini model for that language
Step 3 → translate_text() — produce English translation
Step 4 → translate_text() — produce regional language translation
Step 5 → transliterate_to_script() — if original is spoken (no native script),
          produce a romanized transliteration for phonetic preservation

IMPORTANT GUIDELINES:
- Do NOT over-translate. If a word has no English equivalent, keep the original
  word and add a bracketed explanation. Example: "Pola [bull-worshipping festival]"
- Preserve the speaker's rhythm and idiom. Literal accuracy < cultural faithfulness.
- Flag any words that are unique to this language with [UNIQUE_TERM] marker —
  these are linguistically valuable and should be highlighted in the archive.
- Return output as JSON with keys:
  {
    "original": "...",
    "language_code": "...",
    "dialect": "...",
    "english": "...",
    "regional": "...",
    "transliteration": "...",
    "unique_terms": ["term1", "term2"]
  }
"""

transcription_agent = Agent(
    name="transcription_translation",
    model="gemini-2.5-flash-lite",
    description="Transcribes and translates content in endangered Indian languages.",
    instruction=TRANSCRIPTION_SYSTEM_PROMPT,
    tools=[
        detect_language_tool,
        translate_text_tool,
        transliterate_tool,
        low_resource_model_tool,
    ],
)
