"""
VaakKalp - Cultural Knowledge Graph MCP Server
Provides cultural annotations for festivals, practices, and historical events.
Demonstrates: Custom knowledge base as MCP Server (Day 2).
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


# Curated cultural knowledge base — seed data for demo
# In production: expand with Anthropological Survey of India data, Wikipedia API
FESTIVALS = {
    "pola": {
        "name": "Pola",
        "type": "festival",
        "communities": ["Marathi", "Maharashtra"],
        "description": "A Maharashtrian festival where bulls and bullocks are decorated "
                       "with garlands and worshipped. Marks the end of the sowing season. "
                       "Farmers express deep gratitude to cattle for their indispensable "
                       "role in agriculture.",
        "significance": "Reflects the agrarian roots of Maharashtra and the sacred bond "
                        "between farming communities and their cattle.",
        "typically_in": "Shravan month (July-August)",
    },
    "hornbill": {
        "name": "Hornbill Festival",
        "type": "festival",
        "communities": ["Naga tribes", "Nagaland"],
        "description": "Annual inter-tribal cultural festival of Nagaland celebrating the "
                       "cultural heritage of all Naga tribes. Named after the Great "
                       "Hornbill, a revered bird in Naga folklore.",
        "significance": "One of India's most important tribal cultural events. "
                        "Preserves warrior dances, folk songs, and traditions.",
        "typically_in": "December",
    },
    "onam": {
        "name": "Onam",
        "type": "festival",
        "communities": ["Malayali", "Kerala"],
        "description": "Kerala's harvest festival celebrating the homecoming of the "
                       "mythical King Mahabali. Celebrated with elaborate flower carpets "
                       "(pookalam), boat races, and the grand Onam Sadhya feast.",
        "significance": "Transcends caste and religion — celebrated by all Keralites "
                        "as a symbol of cultural unity and prosperity.",
        "typically_in": "August-September (Chingam month)",
    },
}

TRADITIONAL_PRACTICES = {
    "warli_painting": {
        "name": "Warli Painting",
        "type": "art_craft",
        "community": "Warli tribe, Palghar, Maharashtra",
        "description": "Ancient tribal art using geometric shapes — triangles, circles, "
                       "and squares — to depict scenes of daily life, harvest, hunting, "
                       "and worship. Traditionally painted on mud walls using rice paste.",
        "significance": "One of the oldest art traditions in India, dating to 3000 BCE. "
                        "Now recognized globally but traditionally passed through oral "
                        "and visual teaching within families.",
        "endangered": True,
    },
    "toda_dairy": {
        "name": "Toda Dairy Rituals",
        "type": "religious_practice",
        "community": "Toda, Nilgiri Hills",
        "description": "The Toda community maintains sacred dairy temples (ti) where "
                       "rituals involving buffalo milk are performed. The dairyman-priest "
                       "(palol) undergoes strict ritual purity. Buffalo are considered "
                       "sacred and buffalo funerals are elaborate ceremonies.",
        "significance": "Central to Toda cosmology and identity. The buffalo-dairy "
                        "ritual complex is unique among all world cultures.",
        "endangered": True,
    },
    "chhau_dance": {
        "name": "Chhau Dance",
        "type": "performing_art",
        "community": "Tribal communities of Jharkhand, West Bengal, Odisha",
        "description": "Semi-classical Indian dance with martial and folk traditions. "
                       "Performers wear elaborate masks (in Seraikela and Purulia styles). "
                       "Depicts episodes from the Mahabharata, Ramayana, and local folklore.",
        "significance": "UNESCO Intangible Cultural Heritage. Requires years of training "
                        "and is passed from master to student within families.",
        "endangered": False,
    },
}

HISTORICAL_EVENTS = {
    "partition_1947": {
        "name": "Partition of India (1947)",
        "type": "historical_event",
        "period": "1947",
        "description": "The division of British India into two independent nations — "
                       "India and Pakistan — on August 14-15, 1947. Resulted in one of "
                       "the largest human migrations in history (10-20 million people) "
                       "and widespread communal violence.",
        "impact": "Profound and permanent. Entire communities displaced. "
                  "Languages, traditions, and cultural continuities broken.",
    },
    "drought_vidarbha": {
        "name": "Vidarbha Droughts (1990s-2000s)",
        "type": "agricultural_crisis",
        "period": "1990s–2000s",
        "description": "Severe drought and crop failures in the Vidarbha region of "
                       "Maharashtra led to a widespread farmer suicide crisis. "
                       "Thousands of cotton farmers lost their livelihoods as water "
                       "scarcity combined with debt became insurmountable.",
        "impact": "Demographic shifts, abandonment of traditional farming practices, "
                  "accelerated migration to cities.",
    },
}


@mcp.tool()
def annotate_cultural_reference(text_snippet: str) -> dict:
    """
    Identify and annotate cultural references in a text snippet.

    Args:
        text_snippet: A sentence or passage to analyze for cultural references.

    Returns:
        Detected references with annotations and context.
    """
    text_lower = text_snippet.lower()
    annotations = []

    # Check festivals
    for key, festival in FESTIVALS.items():
        if key in text_lower or festival["name"].lower() in text_lower:
            annotations.append({
                "term": festival["name"],
                "type": "festival",
                "annotation": festival["description"],
                "significance": festival["significance"],
            })

    # Check practices
    for key, practice in TRADITIONAL_PRACTICES.items():
        for term in key.split("_"):
            if term in text_lower and len(term) > 4:
                annotations.append({
                    "term": practice["name"],
                    "type": practice["type"],
                    "annotation": practice["description"],
                    "endangered": practice.get("endangered", False),
                })
                break

    # Check historical events
    for key, event in HISTORICAL_EVENTS.items():
        if any(kw in text_lower for kw in ["partition", "1947", "drought",
                                            "famine", "migration"]):
            if "partition" in text_lower and "partition" in key:
                annotations.append({
                    "term": event["name"],
                    "type": "historical_event",
                    "annotation": event["description"],
                    "period": event["period"],
                })

    return {
        "input_text": text_snippet,
        "annotations_found": len(annotations),
        "annotations": annotations,
    }


@mcp.tool()
def get_festival_info(festival_name: str, region: str = "") -> dict:
    """
    Get detailed information about a festival.

    Args:
        festival_name: Name of the festival
        region: Optional region to narrow results

    Returns:
        Festival details and cultural significance.
    """
    key = festival_name.lower().replace(" ", "_")
    if key in FESTIVALS:
        return FESTIVALS[key]
    # Fuzzy match
    for k, v in FESTIVALS.items():
        if festival_name.lower() in v["name"].lower():
            return v
    return {
        "name": festival_name,
        "note": f"Festival '{festival_name}' not in knowledge base. "
                "This may be a hyper-local tradition — valuable for documentation.",
        "type": "unknown_local_festival",
    }


@mcp.tool()
def get_historical_event(
    event_hint: str,
    region: str = "",
    decade: str = "",
) -> dict:
    """
    Get information about a historical event based on contextual hints.

    Args:
        event_hint: Keywords hinting at the event (e.g., "partition", "drought")
        region: Optional region for context
        decade: Optional decade (e.g., "1940s", "1990s")

    Returns:
        Historical event details and community impact.
    """
    hint_lower = event_hint.lower()
    for key, event in HISTORICAL_EVENTS.items():
        if (any(kw in hint_lower for kw in key.split("_")) or
                decade in event.get("period", "")):
            return event
    return {
        "event_hint": event_hint,
        "note": f"Event not in knowledge base. "
                "Consider flagging for local historian review.",
    }


@mcp.tool()
def get_traditional_practice(practice_description: str) -> dict:
    """
    Get information about a traditional practice from a description.

    Args:
        practice_description: Description or name of the practice

    Returns:
        Practice details and cultural context.
    """
    desc_lower = practice_description.lower()
    for key, practice in TRADITIONAL_PRACTICES.items():
        if any(term in desc_lower for term in key.split("_") if len(term) > 3):
            return practice
    return {
        "description": practice_description,
        "note": "Practice not in knowledge base — this may be a rare local tradition. "
                "Flagged for ethnographic specialist review.",
        "type": "undocumented_practice",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
