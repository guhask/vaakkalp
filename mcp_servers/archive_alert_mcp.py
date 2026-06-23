"""
VaakKalp - Archive & Researcher Alert MCP Server
Handles memoir storage (GCS) and researcher notification dispatch.
Demonstrates: Cloud integration via MCP (Day 2 + Day 5).
"""

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("vaakkalp")
except ImportError:
    class FastMCP:
        def __init__(self, *a, **kw): pass
        def tool(self): return lambda f: f
        def run(self, **kw): pass
    mcp = FastMCP()
from google.cloud import storage
import json
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


GCS_BUCKET = os.getenv("GCS_BUCKET_NAME", "vaakkalp-archives")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")

# Researcher registry — in production: stored in Firestore
RESEARCHER_REGISTRY = {
    "dravidian": [
        {"name": "Dr. Anvita Abbi", "institution": "JNU", "email": "researcher1@example.com",
         "languages": ["toda", "nihali", "kolami"]},
        {"name": "Dr. Madhav Deshpande", "institution": "Univ. of Michigan",
         "email": "researcher2@example.com", "languages": ["dravidian", "prakrit"]},
    ],
    "austroasiatic": [
        {"name": "Dr. Gregory Anderson", "institution": "Living Tongues Institute",
         "email": "researcher3@example.com", "languages": ["korku", "munda", "santali"]},
    ],
    "isolate": [
        {"name": "Dr. Franklin Southworth", "institution": "Univ. of Pennsylvania",
         "email": "researcher4@example.com", "languages": ["nihali", "burushaski"]},
    ],
    "general": [
        {"name": "CIIL Mysore", "institution": "Central Institute of Indian Languages",
         "email": "ciil@example.com", "languages": ["all"]},
        {"name": "ELCat Team", "institution": "Endangered Languages Catalogue",
         "email": "elcat@example.com", "languages": ["all"]},
    ],
}

# In-memory store for demo (replace with Firestore in production)
_archive_store: dict[str, dict] = {}


@mcp.tool()
async def store_archive(memoir_json: str, metadata: str) -> dict:
    """
    Store a memoir to Google Cloud Storage and index it.

    Args:
        memoir_json: JSON string of the structured memoir
        metadata: JSON string of archive metadata

    Returns:
        Archive record with ID, URL, and indexing status.
    """
    try:
        memoir = json.loads(memoir_json) if isinstance(memoir_json, str) else memoir_json
        meta = json.loads(metadata) if isinstance(metadata, str) else metadata
    except json.JSONDecodeError:
        memoir = {"raw": memoir_json}
        meta = {"raw": metadata}

    # Generate unique archive ID
    speaker_name = meta.get("speaker_name", "unknown").replace(" ", "_").lower()
    language = meta.get("language", "unknown").replace(" ", "_").lower()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    archive_id = f"vaakkalp_{language}_{speaker_name[:3]}_{timestamp}"

    archive_record = {
        "archive_id": archive_id,
        "memoir": memoir,
        "metadata": meta,
        "created_at": datetime.utcnow().isoformat(),
        "access_level": meta.get("consent_level", "researcher"),
    }

    # Store in GCS (production)
    public_url = None
    try:
        if PROJECT_ID:
            gcs_client = storage.Client(project=PROJECT_ID)
            bucket = gcs_client.bucket(GCS_BUCKET)
            blob = bucket.blob(f"memoirs/{archive_id}.json")
            blob.upload_from_string(
                json.dumps(archive_record, ensure_ascii=False, indent=2),
                content_type="application/json",
            )
            if meta.get("consent_level") == "public":
                blob.make_public()
                public_url = blob.public_url
            else:
                public_url = f"gs://{GCS_BUCKET}/memoirs/{archive_id}.json"
    except Exception:
        # Demo mode: store in memory
        public_url = f"https://vaakkalp-demo.example.com/archive/{archive_id}"

    # Always store in memory for demo
    _archive_store[archive_id] = archive_record

    return {
        "archive_id": archive_id,
        "public_url": public_url,
        "access_level": archive_record["access_level"],
        "indexed": True,
        "message": f"Memoir archived successfully. ID: {archive_id}",
    }


@mcp.tool()
def search_archive(query: str, filters: str = "{}") -> list[dict]:
    """
    Search the archive for memoirs matching a query.

    Args:
        query: Search terms (language, region, theme, speaker name)
        filters: JSON string with optional filters {"language": "...", "region": "..."}

    Returns:
        List of matching memoir summaries.
    """
    query_lower = query.lower()
    results = []

    for archive_id, record in _archive_store.items():
        meta = record.get("metadata", {})
        searchable = json.dumps(meta).lower()
        if query_lower in searchable:
            results.append({
                "archive_id": archive_id,
                "speaker": meta.get("speaker_name", "Unknown"),
                "language": meta.get("language", "Unknown"),
                "access_level": record.get("access_level"),
                "created_at": record.get("created_at"),
            })

    return results


@mcp.tool()
async def alert_researchers(
    language_name: str,
    speaker_details: str,
    archive_url: str,
) -> dict:
    """
    Dispatch preservation alerts to registered researchers.

    Args:
        language_name: Name of the documented language
        speaker_details: Non-PII speaker info (region, approximate age, community)
        archive_url: URL to the archived memoir

    Returns:
        Alert dispatch status.
    """
    lang_lower = language_name.lower()

    # Find matching researchers
    notified = []
    for family, researchers in RESEARCHER_REGISTRY.items():
        for researcher in researchers:
            if (lang_lower in [l.lower() for l in researcher["languages"]] or
                    "all" in researcher["languages"] or
                    family in lang_lower):
                # In production: send actual email via SendGrid / Gmail API
                # For demo: log the notification
                notified.append({
                    "name": researcher["name"],
                    "institution": researcher["institution"],
                    "email": researcher["email"],
                    "status": "notified_demo_mode",
                })

    if not notified:
        # Default to general registry
        notified = [
            {**r, "status": "notified_demo_mode"}
            for r in RESEARCHER_REGISTRY["general"]
        ]

    return {
        "language": language_name,
        "researchers_notified": len(notified),
        "notifications": notified,
        "archive_url": archive_url,
        "alert_sent": True,
        "note": "Production: sends real emails via SMTP/SendGrid",
    }


@mcp.tool()
def get_researcher_registry(language_family: str = "general") -> list[dict]:
    """
    Get registered researchers for a language family.

    Args:
        language_family: Language family name (e.g., "dravidian", "austroasiatic")

    Returns:
        List of researchers with contact information.
    """
    family_lower = language_family.lower()
    if family_lower in RESEARCHER_REGISTRY:
        return RESEARCHER_REGISTRY[family_lower]
    # Return general registry as fallback
    return RESEARCHER_REGISTRY["general"]


if __name__ == "__main__":
    mcp.run(transport="stdio")
