import asyncio
import aiohttp
import discord
from discord.ext import commands

async def test_site_connection():
    async with aiohttp.ClientSession() as session:
        try:
            # Test script fetch
            url = "https://your-admin-panel.onrender.com/api/scripts/get/test_script"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Successfully fetched script from admin panel")
                    print(f"Script version: {data.get('version', 'N/A')}")
                else:
                    print(f"❌ Failed to fetch script: {response.status}")
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_site_connection())