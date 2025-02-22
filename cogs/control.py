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
        """Set up an advanced control panel with premium features"""
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

            # Create premium control panel embed
            panel = discord.Embed(
                title="🌟 Crystal Hub Premium Control Panel",
                description="Welcome to your premium dashboard",
                color=discord.Color.from_rgb(147, 112, 219)
            )
            
            # Add dynamic statistics
            panel.add_field(
                name="📊 Server Statistics",
                value=f"Members: {interaction.guild.member_count}\nPremium Users: {len(interaction.guild.get_role(config['roles']['premium']).members)}",
                inline=True
            )
            
            # Add feature controls
            panel.add_field(
                name="🎮 Quick Controls",
                value="🔒 - Lock all channels\n🔓 - Unlock all channels\n🎯 - Toggle verification\n⚡ - Boost mode",
                inline=True
            )
            
            # Add premium features
            panel.add_field(
                name="💎 Premium Features",
                value="• Advanced Analytics\n• Auto-moderation\n• Custom Commands\n• Priority Support",
                inline=False
            )

            # Send panel with buttons
            message = await interaction.channel.send(embed=panel)
            
            # Add control reactions
            controls = ['🔒', '🔓', '🎯', '⚡']
            for control in controls:
                await message.add_reaction(control)

            await interaction.followup.send("Control panel created successfully!")

        except Exception as e:
            await interaction.followup.send(f"Error: {str(e)}")

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