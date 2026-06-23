"""
VaakKalp - UNESCO Language Atlas MCP Server
Provides language vitality data and endangered language information.
Demonstrates: Custom MCP Server implementation (Day 2).

In production: wrap UNESCO Atlas of World Languages in Danger API.
For demo: uses a curated dataset of Indian endangered languages.
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
import json


# Curated dataset of endangered Indian languages for demo
# In production: replace with live UNESCO API calls
ENDANGERED_LANGUAGES_DB = {
    "toda": {
        "name": "Toda",
        "language_family": "Dravidian",
        "region": "Nilgiri Hills, Tamil Nadu",
        "speaker_count": 1500,
        "vitality_score": 0.12,
        "risk_level": "CRITICAL",
        "writing_system": "None (oral only)",
        "iso_code": "tcx",
        "documentation_priority": 0.95,
        "notes": "Proto-South-Dravidian language. Spoken by the Toda pastoral community.",
    },
    "nihali": {
        "name": "Nihali",
        "language_family": "Language Isolate",
        "region": "Nimar region, Madhya Pradesh",
        "speaker_count": 2000,
        "vitality_score": 0.08,
        "risk_level": "CRITICAL",
        "writing_system": "None (oral only)",
        "iso_code": "nll",
        "documentation_priority": 0.98,
        "notes": "Complete language isolate — unrelated to any known language family.",
    },
    "gondi": {
        "name": "Gondi",
        "language_family": "Dravidian",
        "region": "Central India (MP, Maharashtra, Odisha, Telangana)",
        "speaker_count": 2900000,
        "vitality_score": 0.45,
        "risk_level": "VULNERABLE",
        "writing_system": "Gondi script (limited use), Devanagari",
        "iso_code": "gon",
        "documentation_priority": 0.60,
        "notes": "Largest tribal language in India but under pressure from Hindi.",
    },
    "bo": {
        "name": "Bo",
        "language_family": "Andamanese",
        "region": "Andaman Islands",
        "speaker_count": 0,
        "vitality_score": 0.0,
        "risk_level": "EXTINCT",
        "writing_system": "None",
        "iso_code": "xbo",
        "documentation_priority": 0.0,
        "notes": "Extinct. Last speaker Boa Sr died in 2010. 65,000+ year old language.",
    },
    "kolami": {
        "name": "Kolami",
        "language_family": "Dravidian",
        "region": "Maharashtra, Andhra Pradesh, Telangana",
        "speaker_count": 100000,
        "vitality_score": 0.35,
        "risk_level": "ENDANGERED",
        "writing_system": "Telugu script",
        "iso_code": "kfb",
        "documentation_priority": 0.72,
        "notes": "Tribal language under heavy influence from Marathi and Telugu.",
    },
    "korku": {
        "name": "Korku",
        "language_family": "Munda (Austroasiatic)",
        "region": "Satpura Hills, MP and Maharashtra",
        "speaker_count": 600000,
        "vitality_score": 0.38,
        "risk_level": "VULNERABLE",
        "writing_system": "Devanagari",
        "iso_code": "kfq",
        "documentation_priority": 0.55,
        "notes": "One of the oldest language families in India. Under threat from Hindi.",
    },
}


@mcp.tool()
def get_language_status(language_name: str) -> dict:
    """
    Get UNESCO vitality status for a language.

    Args:
        language_name: Name of the language (e.g., "Toda", "Nihali")

    Returns:
        Language vitality data including speaker count, risk level, and score.
    """
    key = language_name.lower().strip()
    if key in ENDANGERED_LANGUAGES_DB:
        return ENDANGERED_LANGUAGES_DB[key]

    # Default: unknown language — treat as needing documentation
    return {
        "name": language_name,
        "language_family": "Unknown",
        "region": "Unknown",
        "speaker_count": -1,
        "vitality_score": -1,
        "risk_level": "UNKNOWN — manual review needed",
        "writing_system": "Unknown",
        "iso_code": "und",
        "documentation_priority": 0.8,
        "notes": f"Language '{language_name}' not found in atlas. "
                 "This may be an extremely rare or locally named dialect. "
                 "High documentation priority recommended.",
    }


@mcp.tool()
def list_endangered_languages(region: str = "India") -> list[dict]:
    """
    List all critically endangered or endangered languages for a region.

    Args:
        region: Geographic region to filter by (default: "India")

    Returns:
        List of languages matching the region with their vitality data.
    """
    INDIA_REGIONS = [
        "india", "tamil nadu", "maharashtra", "andhra pradesh", "telangana",
        "madhya pradesh", "mp", "odisha", "jharkhand", "andaman", "kerala",
        "karnataka", "rajasthan", "gujarat", "nagaland", "manipur", "assam",
        "nilgiri", "satpura", "nimar", "central india",
    ]
    region_lower = region.lower()
    results = []
    for lang in ENDANGERED_LANGUAGES_DB.values():
        lang_region_lower = lang["region"].lower()
        # Match if query region found in lang region OR lang region contains any India keyword
        region_match = (
            region_lower in lang_region_lower or
            (region_lower == "india" and
             any(r in lang_region_lower for r in INDIA_REGIONS))
        )
        if region_match and lang["risk_level"] in ("CRITICAL", "ENDANGERED"):
            results.append({
                "name": lang["name"],
                "speaker_count": lang["speaker_count"],
                "risk_level": lang["risk_level"],
                "region": lang["region"],
            })
    return sorted(results, key=lambda x: x["speaker_count"])


@mcp.tool()
def get_documentation_priority(language_name: str) -> dict:
    """
    Get urgency score for documenting a language (0=low, 1=critical).

    Args:
        language_name: Name of the language

    Returns:
        Priority score and recommendation.
    """
    status = get_language_status(language_name)
    priority = status.get("documentation_priority", 0.5)

    if priority >= 0.9:
        recommendation = "DOCUMENT IMMEDIATELY — language may be lost within a decade"
    elif priority >= 0.7:
        recommendation = "HIGH PRIORITY — systematic documentation campaign needed"
    elif priority >= 0.5:
        recommendation = "MODERATE PRIORITY — ongoing documentation recommended"
    else:
        recommendation = "LOWER PRIORITY — language has some vitality but monitor"

    return {
        "language": language_name,
        "priority_score": priority,
        "recommendation": recommendation,
        "speaker_count": status.get("speaker_count", "Unknown"),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
