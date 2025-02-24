import aiohttp
from datetime import datetime

class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    async def notify_script_update(self, script_name, version, action="updated"):
        embed = {
            "title": f"Script {action.title()} 📝",
            "description": f"**Script:** {script_name}\n**Version:** {version}",
            "color": 0x9370DB,
            "timestamp": datetime.utcnow().isoformat()
        }

        async with aiohttp.ClientSession() as session:
            await session.post(
                self.webhook_url,
                json={"embeds": [embed]}
            )