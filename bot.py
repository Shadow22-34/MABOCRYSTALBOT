import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import json
import aiofiles
from datetime import datetime, timedelta
import random
from discord import app_commands

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Constants
CONTROL_PANEL_CHANNEL_ID = int(os.getenv('CONTROL_PANEL_CHANNEL_ID', 0))
BUYER_ROLE_ID = int(os.getenv('BUYER_ROLE_ID', 0))
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID', 0))

# Initialize data structures
hwid_data = {
    "users": {},  # Store user HWIDs
    "resets": {},  # Track HWID resets
    "blacklist": []
}

class CrystalBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            help_command=None
        )
        
    async def setup_hook(self):
        # Create cogs directory if it doesn't exist
        if not os.path.exists('./cogs'):
            os.makedirs('./cogs')
            print("Created cogs directory")
        
        # Load cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename}')
        
        # Sync commands with all guilds
        print("Syncing commands...")
        await self.tree.sync()
        print("Synced command tree")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Crystal Hub Premium"
            )
        )

# Initialize bot
bot = CrystalBot()

# Basic error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"This command is on cooldown. Try again in {error.retry_after:.2f}s",
            ephemeral=True
        )
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "You don't have permission to use this command!",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"An error occurred: {str(error)}",
            ephemeral=True
        )
        print(f"Error in {interaction.command.name}: {str(error)}")

# Run bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)