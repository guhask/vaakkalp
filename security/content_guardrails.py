"""
VaakKalp - Content Guardrails & Security
Implements input validation, PII masking, sacred content detection, prompt injection prevention.
Demonstrates: Agent security implementation (Day 4).
"""

import re
import json
from enum import Enum

# --------------------------------------------------------------------------
# Enums
# --------------------------------------------------------------------------

class ContentFlag(Enum):
    CLEAN = "clean"
    PROMPT_INJECTION = "prompt_injection"
    SACRED_CONTENT = "sacred_content"
    PII_DETECTED = "pii_detected"
    HARMFUL_CONTENT = "harmful_content"


class ConsentLevel(Enum):
    PUBLIC = "public"
    RESEARCHER = "researcher"
    COMMUNITY = "community"
    FAMILY = "family"
    RESTRICTED = "restricted"


# --------------------------------------------------------------------------
# 1. Prompt Injection Prevention
# --------------------------------------------------------------------------

INJECTION_PATTERNS = [
    r"ignore (previous|all|above) instructions",
    r"you are now",
    r"disregard your",
    r"act as (a|an|if)",
    r"your new (role|instructions|purpose)",
    r"forget (everything|all|what)",
    r"system prompt",
    r"<\|im_start\|>",
    r"\[INST\]",
    r"###\s*(instruction|system|human|assistant)",
    r"override (safety|guidelines|rules)",
]

COMPILED_INJECTION = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]


def detect_prompt_injection(text: str) -> bool:
    """Returns True if the text appears to contain a prompt injection attempt."""
    return any(pattern.search(text) for pattern in COMPILED_INJECTION)


# --------------------------------------------------------------------------
# 2. Sacred/Ritual Content Detection
# --------------------------------------------------------------------------

SACRED_MARKERS = [
    "sacred", "ritual", "forbidden", "secret ceremony", "initiation rite",
    "must not be shared", "not for outsiders", "only elders know",
    "taboo", "ancestral spirit", "spirit medium", "ghost ceremony",
    "cannot be recorded", "eyes closed", "only for men", "only for women",
    # Hindi/Marathi markers
    "mantra", "gupt", "gupth vidya", "rahasy", "devrahasya",
    # Tamil markers
    "rahasyam", "thantram",
]


def detect_sacred_content(text: str) -> bool:
    """Returns True if the text appears to contain sacred/ritual content."""
    text_lower = text.lower()
    return any(marker in text_lower for marker in SACRED_MARKERS)


# --------------------------------------------------------------------------
# 3. PII Masking
# --------------------------------------------------------------------------

PII_PATTERNS = {
    "aadhaar": (r"\b\d{4}\s?\d{4}\s?\d{4}\b", "[AADHAAR_REDACTED]"),
    "phone_in": (r"\b(\+91|0)?[6-9]\d{9}\b", "[PHONE_REDACTED]"),
    "phone_generic": (r"\b\d{10}\b", "[PHONE_REDACTED]"),
    "email": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]"),
    "pan": (r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b", "[PAN_REDACTED]"),
}

COMPILED_PII = {
    name: (re.compile(pattern), replacement)
    for name, (pattern, replacement) in PII_PATTERNS.items()
}


def mask_pii(text: str) -> tuple[str, list[str]]:
    """
    Masks PII from text. Returns (cleaned_text, list_of_pii_types_found).
    """
    found_pii = []
    cleaned = text
    for pii_type, (pattern, replacement) in COMPILED_PII.items():
        new_text = pattern.sub(replacement, cleaned)
        if new_text != cleaned:
            found_pii.append(pii_type)
            cleaned = new_text
    return cleaned, found_pii


# --------------------------------------------------------------------------
# 4. Harmful Content Filter
# --------------------------------------------------------------------------

HARMFUL_PATTERNS = [
    r"\b(weapon|bomb|explosive|kill|murder|harm|attack)\b",
    r"(how to|instructions for|steps to)\s+(make|create|build)\s+\w+",
]
COMPILED_HARMFUL = [re.compile(p, re.IGNORECASE) for p in HARMFUL_PATTERNS]


def detect_harmful_content(text: str) -> bool:
    """Returns True if the text contains clearly harmful requests."""
    return any(pattern.search(text) for pattern in COMPILED_HARMFUL)


# --------------------------------------------------------------------------
# 5. Main Guardrail Pipeline
# --------------------------------------------------------------------------

def apply_guardrails(user_input: str) -> str:
    """
    Main security pipeline. Validates input before it reaches the agent.

    Returns:
        Sanitized input string (safe to pass to agent).

    Raises:
        ValueError: If input contains prompt injection or harmful content.
    """
    if not user_input or not user_input.strip():
        raise ValueError("Empty input received.")

    # Check length (prevent token flooding attacks)
    if len(user_input) > 10000:
        user_input = user_input[:10000] + "\n[INPUT_TRUNCATED_FOR_SAFETY]"

    # 1. Prompt injection check
    if detect_prompt_injection(user_input):
        raise ValueError(
            "SECURITY: Potential prompt injection detected. "
            "Please share your story naturally — no special instructions needed."
        )

    # 2. Harmful content check
    if detect_harmful_content(user_input):
        raise ValueError(
            "SECURITY: Input flagged for review. "
            "VaakKalp is designed to record stories and cultural memories."
        )

    # 3. PII masking (don't raise — just clean silently)
    cleaned_input, found_pii = mask_pii(user_input)
    if found_pii:
        # Log PII detection (don't expose to user)
        print(f"[SECURITY] PII masked from input: {found_pii}")

    # 4. Sacred content detection (flag, don't block — let agent handle)
    if detect_sacred_content(cleaned_input):
        cleaned_input = f"[SACRED_CONTENT_FLAG] {cleaned_input}"

    return cleaned_input


def apply_output_guardrails(agent_output: str, consent_level: str) -> str:
    """
    Validates agent output before it reaches the user.
    Applies additional PII masking to outputs for non-family consent levels.
    """
    if consent_level in ("public", "researcher", "community"):
        cleaned, _ = mask_pii(agent_output)
        return cleaned
    return agent_output


# --------------------------------------------------------------------------
# 6. Consent Manager
# --------------------------------------------------------------------------

class ConsentManager:
    """Manages digitally logged consent for each recording session."""

    @staticmethod
    def create_consent_record(
        speaker_name: str,
        language: str,
        consent_level: str,
        session_id: str,
        sacred_content_excluded: bool = True,
    ) -> dict:
        """Create a consent record at the start of a session."""
        from datetime import datetime
        return {
            "session_id": session_id,
            "speaker_name": speaker_name,
            "language": language,
            "consent_level": ConsentLevel(consent_level).value,
            "sacred_content_excluded": sacred_content_excluded,
            "timestamp": datetime.utcnow().isoformat(),
            "consent_given": True,
            "right_to_withdraw": True,
            "data_sovereignty": "community_owned",
        }

    @staticmethod
    def validate_access(
        archive_consent_level: str,
        requester_role: str,
    ) -> bool:
        """Check if a requester can access an archive based on consent level."""
        access_matrix = {
            ConsentLevel.PUBLIC.value: ["public", "researcher", "community", "family", "admin"],
            ConsentLevel.RESEARCHER.value: ["researcher", "community", "family", "admin"],
            ConsentLevel.COMMUNITY.value: ["community", "family", "admin"],
            ConsentLevel.FAMILY.value: ["family", "admin"],
            ConsentLevel.RESTRICTED.value: ["admin"],
        }
        allowed_roles = access_matrix.get(archive_consent_level, [])
        return requester_role in allowed_roles
