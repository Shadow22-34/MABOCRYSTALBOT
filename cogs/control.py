import discord
from discord.ext import commands
from discord import app_commands
import json
import aiofiles

class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="controlpanel")
    @app_commands.checks.has_permissions(administrator=True)
    async def controlpanel(self, interaction: discord.Interaction):
        """Set up the control panel"""
        await interaction.response.send_message("Control panel setup coming soon!", ephemeral=True)

    @app_commands.command(name="addbuyer")
    @app_commands.checks.has_permissions(administrator=True)
    async def addbuyer(self, interaction: discord.Interaction, user: discord.Member):
        """Add a premium user"""
        try:
            # Load config
            async with aiofiles.open("server_config.json", "r") as f:
                config = json.loads(await f.read())
            
            premium_role = interaction.guild.get_role(config["roles"]["premium"])
            if premium_role:
                await user.add_roles(premium_role)
                await interaction.response.send_message(f"Added {user.mention} as a premium user!", ephemeral=True)
            else:
                await interaction.response.send_message("Premium role not found. Please run /setup first.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

    @app_commands.command(name="config")
    @app_commands.checks.has_permissions(administrator=True)
    async def config(self, interaction: discord.Interaction):
        """Configure bot settings"""
        await interaction.response.send_message("Configuration options coming soon!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ControlPanel(bot))