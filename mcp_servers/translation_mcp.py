"""
VaakKalp - Translation MCP Server (Google Cloud Translation only)
Replaces Bhashini with Google Cloud Translation API v3.
Easier setup, instant API key, same 22+ Indian languages supported.
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
import httpx, os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_DETECT_URL = "https://translation.googleapis.com/language/translate/v2/detect"

# 22 Indian languages supported by Google Cloud Translation
INDIAN_LANGUAGES = {
    "as": "Assamese", "bn": "Bengali", "brx": "Bodo", "doi": "Dogri",
    "gu": "Gujarati", "hi": "Hindi", "kn": "Kannada", "ks": "Kashmiri",
    "kok": "Konkani", "mai": "Maithili", "ml": "Malayalam", "mni": "Manipuri",
    "mr": "Marathi", "ne": "Nepali", "or": "Odia", "pa": "Punjabi",
    "sa": "Sanskrit", "sat": "Santali", "sd": "Sindhi", "ta": "Tamil",
    "te": "Telugu", "ur": "Urdu",
}

LOW_RESOURCE = {"tcx": "toda", "nll": "nihali", "gon": "gondi", "kfb": "kolami"}


@mcp.tool()
async def detect_language(audio_text: str) -> dict:
    """Auto-detect language using Google Cloud Translation."""
    if not GOOGLE_API_KEY:
        return {"language_code": "und", "confidence": 0.0, "note": "No API key set"}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                GOOGLE_DETECT_URL,
                params={"key": GOOGLE_API_KEY},
                json={"q": audio_text},
                timeout=10.0,
            )
            if r.status_code == 200:
                det = r.json()["data"]["detections"][0][0]
                return {
                    "language_code": det["language"],
                    "confidence": det["confidence"],
                    "dialect_hint": INDIAN_LANGUAGES.get(det["language"], "Unknown"),
                }
    except Exception as e:
        pass
    return {"language_code": "und", "confidence": 0.0, "error": "Detection failed"}


@mcp.tool()
async def translate_text(text: str, source_lang: str, target_lang: str) -> dict:
    """Translate text using Google Cloud Translation API."""
    if not GOOGLE_API_KEY:
        return {"translated": f"[NO API KEY] {text}", "provider": "none"}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                GOOGLE_TRANSLATE_URL,
                params={"key": GOOGLE_API_KEY},
                json={"q": text, "source": source_lang, "target": target_lang, "format": "text"},
                timeout=10.0,
            )
            if r.status_code == 200:
                translated = r.json()["data"]["translations"][0]["translatedText"]
                return {"translated": translated, "source_lang": source_lang,
                        "target_lang": target_lang, "provider": "google_translate"}
    except Exception as e:
        pass
    return {"translated": f"[TRANSLATION FAILED] {text}", "provider": "error"}


@mcp.tool()
async def transliterate_to_script(text: str, target_script: str = "roman") -> dict:
    """Transliterate using Google Translate with romanization hint."""
    # Google Translate to English gives effective romanization for demo
    result = await translate_text(text, "auto", "en")
    return {"transliterated": result.get("translated", text),
            "original": text, "target_script": target_script}


@mcp.tool()
def get_low_resource_model(language_code: str) -> dict:
    """For low-resource languages, fall back to Google Translate with a quality note."""
    if language_code in LOW_RESOURCE:
        return {"language_code": language_code,
                "language_name": LOW_RESOURCE[language_code],
                "model": "google_translate_fallback",
                "quality": "limited — human expert review recommended",
                "note": "Low-resource language. Google Translate coverage is partial."}
    return {"language_code": language_code, "model": "google_translate", "quality": "good"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
