import asyncio
from mcp_servers.translation_mcp import detect_language, translate_text
async def test():
    text = "मी पुण्यात राहतो"
    lang = await detect_language(text)
    print("Detected:", lang)
    result = await translate_text(text, "mr", "en")
    print("Translated:", result)
asyncio.run(test())
