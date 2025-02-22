import discord
from discord.ext import commands
from discord import app_commands
import json
import aiofiles

class SetupWizard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def create_roles(self, guild):
        roles = {}
        
        # Create Premium role with fancy styling
        premium_role = await guild.create_role(
            name="Crystal Premium",
            color=discord.Color.from_rgb(147, 112, 219),
            hoist=True,
            mentionable=True
        )
        roles["premium"] = premium_role.id
        
        # Create Admin role
        admin_role = await guild.create_role(
            name="Crystal Admin",
            color=discord.Color.from_rgb(255, 0, 0),
            permissions=discord.Permissions.all(),
            hoist=True
        )
        roles["admin"] = admin_role.id
        
        return roles

    async def create_channels(self, guild, roles):
        channels = {}
        
        # Create categories
        crystal_category = await guild.create_category("CRYSTAL HUB")
        
        # Create channels with proper permissions
        channels["control"] = await crystal_category.create_text_channel(
            "control-panel",
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                guild.get_role(roles["premium"]): discord.PermissionOverwrite(read_messages=True),
                guild.get_role(roles["admin"]): discord.PermissionOverwrite(administrator=True)
            }
        )
        
        channels["announcements"] = await crystal_category.create_text_channel(
            "announcements",
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                guild.get_role(roles["admin"]): discord.PermissionOverwrite(send_messages=True)
            }
        )
        
        channels["support"] = await crystal_category.create_text_channel("support")
        
        return channels

    @app_commands.command(name="setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """Initialize Crystal Hub with an epic setup wizard"""
        await interaction.response.defer()
        
        # Setup progress embed
        progress_embed = discord.Embed(
            title="🚀 Crystal Hub Setup",
            description="Initializing setup...",
            color=discord.Color.blue()
        )
        progress_message = await interaction.followup.send(embed=progress_embed)
        
        try:
            # Create roles
            progress_embed.description = "Creating roles..."
            await progress_message.edit(embed=progress_embed)
            roles = await self.create_roles(interaction.guild)
            
            # Create channels
            progress_embed.description = "Creating channels..."
            await progress_message.edit(embed=progress_embed)
            channels = await self.create_channels(interaction.guild, roles)
            
            # Save configuration
            config = {
                "guild_id": interaction.guild.id,
                "roles": roles,
                "channels": channels,
                "is_setup": True
            }
            
            async with aiofiles.open("server_config.json", "w") as f:
                await f.write(json.dumps(config, indent=4))
            
            # Final success message
            success_embed = discord.Embed(
                title="✅ Setup Complete!",
                description="Crystal Hub has been successfully set up!",
                color=discord.Color.green()
            )
            success_embed.add_field(
                name="Next Steps",
                value="1. Use `/controlpanel` to set up the control panel\n2. Add premium users with `/addbuyer`\n3. Configure additional settings with `/config`",
                inline=False
            )
            await progress_message.edit(embed=success_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Setup Failed",
                description=f"Error: {str(e)}",
                color=discord.Color.red()
            )
            await progress_message.edit(embed=error_embed)

async def setup(bot):
    await bot.add_cog(SetupWizard(bot))
