"""
VaakKalp - ADK Event Diagnostics
Run this directly to inspect raw event structure from ADK runner.
Usage: python diagnose.py
"""

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


# Minimal agent for testing
test_agent = Agent(
    name="test_agent",
    model="gemini-2.5-flash-lite",
    description="Test agent",
    instruction="You are a helpful assistant. Reply with a short greeting.",
)

session_service = InMemorySessionService()
runner = Runner(
    agent=test_agent,
    app_name="test",
    session_service=session_service,
)


async def diagnose():
    session = await session_service.create_session(
        app_name="test",
        user_id="test_user",
        session_id="test_session_1",
    )

    content = Content(role="user", parts=[Part(text="Hello, say hi back in one sentence.")])

    print("\n=== STARTING EVENT INSPECTION ===\n")
    event_count = 0

    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session_1",
        new_message=content,
    ):
        event_count += 1
        print(f"\n--- Event #{event_count} ---")
        print(f"  Type         : {type(event).__name__}")
        print(f"  All attrs    : {[a for a in dir(event) if not a.startswith('_')]}")

        # Check is_final_response
        try:
            is_final = event.is_final_response()
            print(f"  is_final     : {is_final}")
        except Exception as e:
            print(f"  is_final ERR : {e}")

        # Check content
        if hasattr(event, "content"):
            print(f"  content      : {event.content}")
            if event.content:
                print(f"  content type : {type(event.content).__name__}")
                print(f"  content attrs: {[a for a in dir(event.content) if not a.startswith('_')]}")
                if hasattr(event.content, "parts"):
                    print(f"  parts        : {event.content.parts}")
                    if event.content.parts:
                        for i, part in enumerate(event.content.parts):
                            print(f"    part[{i}]    : type={type(part).__name__}, attrs={[a for a in dir(part) if not a.startswith('_')]}")
                            if hasattr(part, "text"):
                                print(f"    part[{i}].text: {part.text!r}")
        else:
            print("  content      : (no content attr)")

        # Check for text directly on event
        for attr in ["text", "response", "message", "output", "result"]:
            if hasattr(event, attr):
                print(f"  event.{attr:<10}: {getattr(event, attr)!r}")

    print(f"\n=== DONE: {event_count} events inspected ===\n")


if __name__ == "__main__":
    asyncio.run(diagnose())
