import aiohttp
import json
from datetime import datetime

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1343343812809855108/Al075iHS1EBUFLGw2f-bAe2EE2WqVrc8Owo8qHRcAhQicr_IxUh5Q9MtHZUJE7c7HMLq"

async def send_script_update_alert(script_name: str, action: str, version: str = None):
    embed = {
        "title": f"🔄 Crystal Hub Script {action}",
        "description": f"Script: `{script_name}`\nVersion: `{version or 'N/A'}`",
        "color": 0x9370DB,  # Purple color
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "Crystal Hub Admin Panel"
        }
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(WEBHOOK_URL, json={"embeds": [embed]}) as response:
                if response.status != 204:
                    print(f"Failed to send webhook: {await response.text()}")
                else:
                    print(f"Successfully sent webhook for {script_name}")
        except Exception as e:
            print(f"Error sending webhook: {str(e)}")