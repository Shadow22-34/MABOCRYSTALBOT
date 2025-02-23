import discord
from discord.ext import commands
from discord import app_commands
import json
import aiofiles
from datetime import datetime, timedelta

class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="controlpanel")
    @app_commands.checks.has_permissions(administrator=True)
    async def controlpanel(self, interaction: discord.Interaction):
        """Set up the Crystal Hub Script Control Panel"""
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Create the main panel embed
            panel = discord.Embed(
                title="🌟 Crystal Hub Script Panel",
                description="Use the Buttons Below to use the panel",
                color=discord.Color.from_rgb(147, 112, 219)
            )
            
            # Add script panel section
            panel.add_field(
                name="🔑 Yuna - Script Panel",
                value=(
                    "🔑 Reedeem Key - Claim the key your purchased on Yuna Website\n"
                    "📜 Get Script - Get the main Yuna Loader\n"
                    "📊 Get Stats - Get all your Yuna Stats\n"
                    "⚙️ Reset HWID - Reset your HWID"
                ),
                inline=False
            )
            
            # Add information section
            panel.add_field(
                name="ℹ️ Information",
                value=(
                    "🐛 Report Bugs & Other Script Problems in: #support\n"
                    "💡 Give Suggestions in: #suggestions\n"
                    "⭐ Leave your review in: #reviews using /review\n"
                    "📋 Share configs in: #configs"
                ),
                inline=False
            )

            # Create buttons
            buttons = discord.ui.View()
            buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, label="🔑 Redeem Key", custom_id="redeem_key"))
            buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label="📜 Get Script", custom_id="get_script"))
            buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label="⚡ Get Role", custom_id="get_role"))
            buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.gray, label="⚙️ Reset HWID", custom_id="reset_hwid"))
            buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.gray, label="📊 Get Stats", custom_id="get_stats"))

            # Send panel with buttons
            await interaction.channel.send(embed=panel, view=buttons)
            await interaction.followup.send("Control panel created successfully!")

        except Exception as e:
            await interaction.followup.send(f"Error: {str(e)}")

    # Add button handlers
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if not interaction.type == discord.InteractionType.component:
            return

        try:
            if interaction.custom_id == "redeem_key":
                await self.handle_redeem_key(interaction)
            elif interaction.custom_id == "get_script":
                await self.handle_get_script(interaction)
            elif interaction.custom_id == "get_role":
                await self.handle_get_role(interaction)
            elif interaction.custom_id == "reset_hwid":
                await self.handle_reset_hwid(interaction)
            elif interaction.custom_id == "get_stats":
                await self.handle_get_stats(interaction)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

    async def handle_redeem_key(self, interaction: discord.Interaction):
        # Add key redemption logic here
        await interaction.response.send_modal(
            discord.ui.Modal(
                title="🔑 Redeem Your Key",
                custom_id="key_modal",
                components=[
                    discord.ui.TextInput(
                        label="Enter your key",
                        placeholder="XXXX-XXXX-XXXX-XXXX",
                        custom_id="key_input",
                        style=discord.TextStyle.short,
                        required=True
                    )
                ]
            )
        )

    async def handle_get_script(self, interaction: discord.Interaction):
        # Add script delivery logic here
        await interaction.response.send_message("Here's your Crystal Hub script!", ephemeral=True)

    async def handle_get_role(self, interaction: discord.Interaction):
        # Add role assignment logic here
        await interaction.response.send_message("Assigning buyer role...", ephemeral=True)

    async def handle_reset_hwid(self, interaction: discord.Interaction):
        # Add HWID reset logic here
        await interaction.response.send_message("HWID reset successful!", ephemeral=True)

    async def handle_get_stats(self, interaction: discord.Interaction):
        # Add stats display logic here
        stats_embed = discord.Embed(
            title="📊 Your Crystal Hub Stats",
            color=discord.Color.blue()
        )
        stats_embed.add_field(name="Script Executions", value="0", inline=True)
        stats_embed.add_field(name="Last Used", value="Never", inline=True)
        stats_embed.add_field(name="HWID Status", value="✅ Active", inline=True)
        
        await interaction.response.send_message(embed=stats_embed, ephemeral=True)

    @app_commands.command(name="addbuyer")
    @app_commands.checks.has_permissions(administrator=True)
    async def addbuyer(self, interaction: discord.Interaction, user: discord.Member):
        """Add a premium user with exclusive benefits"""
        # Defer the response first
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Check if setup has been run
            try:
                async with aiofiles.open("server_config.json", "r") as f:
                    config = json.loads(await f.read())
            except FileNotFoundError:
                await interaction.followup.send("Please run `/setup` first to initialize Crystal Hub!")
                return

            premium_role = interaction.guild.get_role(config['roles']['premium'])
            await user.add_roles(premium_role)

            # Create welcome embed
            welcome = discord.Embed(
                title="🎉 Welcome to Crystal Premium!",
                description=f"Welcome {user.mention} to the elite club!",
                color=discord.Color.from_rgb(147, 112, 219)
            )
            
            welcome.add_field(
                name="💎 Your Premium Benefits",
                value="• Exclusive Channel Access\n• Priority Support\n• Custom Commands\n• Advanced Features",
                inline=False
            )
            
            welcome.add_field(
                name="🔥 Quick Start",
                value="• Check #control-panel for features\n• Use /help premium for commands\n• Join premium voice channels",
                inline=False
            )
            
            welcome.set_footer(text="Thank you for choosing Crystal Premium!")
            
            # Send welcome message
            await interaction.channel.send(embed=welcome)
            await interaction.followup.send(f"Successfully added {user.mention} as a premium user!")

        except Exception as e:
            await interaction.followup.send(f"Error: {str(e)}")

    @app_commands.command(name="config")
    @app_commands.checks.has_permissions(administrator=True)
    async def config(self, interaction: discord.Interaction):
        """Configure advanced bot settings"""
        try:
            # Create configuration embed
            config_embed = discord.Embed(
                title="⚙️ Crystal Hub Configuration",
                description="Advanced settings and customization",
                color=discord.Color.blue()
            )
            
            # Add configuration sections
            config_embed.add_field(
                name="🛡️ Security Settings",
                value="• Anti-raid Protection\n• Verification System\n• Auto-moderation\n• Spam Prevention",
                inline=True
            )
            
            config_embed.add_field(
                name="🎨 Customization",
                value="• Custom Commands\n• Welcome Messages\n• Role Management\n• Channel Setup",
                inline=True
            )
            
            config_embed.add_field(
                name="📊 Analytics",
                value="• Member Statistics\n• Activity Tracking\n• Usage Reports\n• Performance Metrics",
                inline=False
            )

            # Send configuration panel
            await interaction.response.send_message(embed=config_embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ControlPanel(bot))