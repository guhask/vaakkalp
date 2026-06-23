"""
VaakKalp - Interview Conductor Agent
Conducts intelligent, culturally sensitive oral history interviews.
Demonstrates: Dynamic tool use, reusable skill (Day 3).
"""

QUESTION_BANK = {
    "childhood":  [
        "Where were you born, and what was your village/town like when you were a child?",
        "What games did you play as a child? Were there any songs or stories told to children?",
        "What do you remember most about your mother and father?",
        "What was the most important festival celebrated in your family when you were young?",
    ],
    "livelihood": [
        "What work did you do through your life? What did your parents do?",
        "Were there any special skills or crafts passed down in your family?",
        "What did the land / river / forest mean to your community's way of life?",
        "How has the nature of work changed from your grandparents' time to today?",
    ],
    "culture": [
        "What festivals, rituals, or ceremonies were most important to your community?",
        "Are there proverbs or sayings in your language that your elders used often?",
        "Were there traditional medicines or healing practices in your community?",
        "What songs do you remember from your childhood? Can you share one?",
    ],
    "history": [
        "What major events happened during your lifetime that changed everything?",
        "What stories did your grandparents tell about life before your time?",
        "How did your community respond to big changes — droughts, floods, or new roads?",
        "Who was the most respected elder in your community, and why?",
    ],
    "philosophy": [
        "What is the most important lesson life has taught you?",
        "What do you wish young people today understood that they seem to have forgotten?",
        "What does a good life look like, in your understanding?",
        "What would you want your grandchildren to remember about you?",
    ],
}

SACRED_MARKERS = [
    "ritual", "sacred", "forbidden", "secret ceremony", "initiation",
    "mantra", "gupt", "rahasy", "only elders know", "must not be shared",
    "not for outsiders", "taboo", "ancestral spirit",
]


def get_next_question(
    current_topic: str,
    questions_asked: list,
    last_response: str,
) -> dict:
    """Returns the next interview question, probing hooks when detected."""
    hooks = ["flood", "fire", "partition", "died", "drought", "war",
             "left", "migration", "famine", "born", "river", "changed"]
    for hook in hooks:
        if hook in last_response.lower():
            return {"question": f"You mentioned '{hook}' — could you tell me more about that?",
                    "topic": current_topic, "is_probe": True}

    available = [q for q in QUESTION_BANK.get(current_topic, []) if q not in questions_asked]
    if available:
        return {"question": available[0], "topic": current_topic, "is_probe": False}

    topics = list(QUESTION_BANK.keys())
    current_index = topics.index(current_topic) if current_topic in topics else 0
    next_topic = topics[(current_index + 1) % len(topics)]
    return {"question": QUESTION_BANK[next_topic][0], "topic": next_topic, "is_probe": False}


def detect_sacred_content(text: str) -> bool:
    """Flags text containing sacred/ritual content requiring restricted access."""
    text_lower = text.lower()
    return any(marker in text_lower for marker in SACRED_MARKERS)


# ADK Agent — only loaded when google-adk is installed
try:
    from google.adk.agents import Agent
    from google.adk.tools import FunctionTool

    interview_conductor_agent = Agent(
        name="interview_conductor",
        model="gemini-2.5-flash-lite",
        description="Conducts intelligent, culturally sensitive oral history interviews.",
        instruction="""
You are VaakKalp's Interview Conductor. Conduct warm, patient oral history interviews.
Use get_next_question() to decide what to ask — NEVER ask more than one question at a time.
Use detect_sacred_content() on every response; if flagged, note it will be stored privately.
Acknowledge what the speaker says before asking the next question. Never rush. Never judge.
""",
        tools=[FunctionTool(get_next_question), FunctionTool(detect_sacred_content)],
    )
except ImportError:
    interview_conductor_agent = None  # type: ignore
