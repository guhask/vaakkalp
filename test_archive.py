import asyncio
from mcp_servers.archive_alert_mcp import store_archive, get_researcher_registry
import json

async def test():
    memoir = json.dumps({'speaker': 'Vasamalli', 'language': 'Toda', 'chapters': []})
    meta = json.dumps({'speaker_name': 'Vasamalli', 'language': 'Toda', 'consent_level': 'researcher'})
    result = await store_archive(memoir, meta)
    print('Archive:', result)
    researchers = get_researcher_registry('dravidian')
    print('Researchers:', researchers)

asyncio.run(test())
