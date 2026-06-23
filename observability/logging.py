"""
VaakKalp - Observability & Logging
Cloud Logging integration for agent event tracing.
Demonstrates: Production observability (Day 5).
"""

import logging
import os
import json
from datetime import datetime

try:
    from google.cloud import logging as cloud_logging
    CLOUD_LOGGING_AVAILABLE = True
except ImportError:
    CLOUD_LOGGING_AVAILABLE = False

# Setup
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")

# Initialize Cloud Logging if available
if CLOUD_LOGGING_AVAILABLE and PROJECT_ID:
    try:
        cloud_client = cloud_logging.Client(project=PROJECT_ID)
        cloud_client.setup_logging()
    except Exception:
        pass

logger = logging.getLogger("vaakkalp")
logging.basicConfig(level=getattr(logging, LOG_LEVEL))


def log_agent_event(
    agent_name: str,
    event_type: str,
    session_id: str,
    metadata: dict | None = None,
) -> None:
    """
    Log a structured agent event to Cloud Logging.

    Args:
        agent_name: Name of the agent generating the event
        event_type: Type of event (e.g., "session_start", "mcp_call", "error")
        session_id: Current session ID
        metadata: Optional additional metadata dict
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent_name,
        "event": event_type,
        "session_id": session_id,
        "service": "vaakkalp",
        **(metadata or {}),
    }

    if event_type.startswith("error"):
        logger.error(json.dumps(log_entry))
    elif event_type in ("session_start", "session_complete", "archive_published"):
        logger.info(json.dumps(log_entry))
    else:
        logger.debug(json.dumps(log_entry))


def log_mcp_call(
    mcp_server: str,
    tool_name: str,
    session_id: str,
    latency_ms: float,
    success: bool,
) -> None:
    """Log MCP tool call performance for monitoring."""
    log_agent_event(
        agent_name=f"mcp_{mcp_server}",
        event_type="mcp_tool_call",
        session_id=session_id,
        metadata={
            "tool": tool_name,
            "latency_ms": latency_ms,
            "success": success,
        },
    )


def log_security_event(
    event_type: str,
    session_id: str,
    details: str,
) -> None:
    """Log security events (injections, PII detections, consent issues)."""
    log_agent_event(
        agent_name="security_layer",
        event_type=f"security_{event_type}",
        session_id=session_id,
        metadata={"details": details},
    )
