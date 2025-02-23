import aiohttp
import json
from datetime import datetime

WEBHOOK_CHANNEL_ID = "1343335241359822982"
WEBHOOK_URL = f"https://discord.com/api/v10/channels/{WEBHOOK_CHANNEL_ID}/messages"

async def send_script_update_alert(script_name: str, action: str, version: str = None):
    embed = {
        "title": f"🔄 Crystal Hub Script {action}",
        "description": f"Script: `{script_name}`\nVersion: `{version or 'N/A'}`",
        "color": 0x9370DB,
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "Crystal Hub Admin Panel"
        }
    }

    async with aiohttp.ClientSession() as session:
        await session.post(WEBHOOK_URL, json={"embeds": [embed]})