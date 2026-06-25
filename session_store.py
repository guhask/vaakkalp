"""
VaakKalp - Persistent Session Store
Saves session state to disk so conversations survive server restarts.
Demonstrates: Long-term memory and state persistence (Day 3).
"""

import json
import os
from pathlib import Path

SESSION_DIR = Path("session_data")
SESSION_DIR.mkdir(exist_ok=True)


def save_session(session_id: str, user_id: str, messages: list) -> None:
    """Save session messages to disk."""
    path = SESSION_DIR / f"{session_id}.json"
    data = {
        "session_id": session_id,
        "user_id": user_id,
        "messages": messages,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_session(session_id: str) -> dict | None:
    """Load session from disk. Returns None if not found."""
    path = SESSION_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def append_message(session_id: str, user_id: str, role: str, text: str) -> None:
    """Append a single message to an existing or new session."""
    existing = load_session(session_id)
    if existing:
        messages = existing["messages"]
    else:
        messages = []
    messages.append({"role": role, "text": text})
    save_session(session_id, user_id, messages)


def get_session_context(session_id: str, max_turns: int = 10) -> str:
    """
    Returns last N turns as a context string to inject into the prompt.
    This gives the agent memory of prior conversation across restarts.
    """
    data = load_session(session_id)
    if not data or not data.get("messages"):
        return ""

    messages = data["messages"][-max_turns * 2:]  # last N turns (user+agent pairs)
    context_lines = ["=== PRIOR CONVERSATION CONTEXT (from previous session) ==="]
    for msg in messages:
        prefix = "Speaker" if msg["role"] == "user" else "VaakKalp"
        context_lines.append(f"{prefix}: {msg['text']}")
    context_lines.append("=== END OF PRIOR CONTEXT — Continue from here ===\n")
    return "\n".join(context_lines)
