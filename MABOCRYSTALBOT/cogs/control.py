class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="controlpanel")
    async def controlpanel(self, interaction: discord.Interaction):
        # Check if user has premium role
        premium_role = discord.utils.get(interaction.guild.roles, id=1343002193321791558)
        if premium_role not in interaction.user.roles:
            await interaction.response.send_message("❌ You need premium to use Crystal Hub!", ephemeral=True)
            return

        embed = discord.Embed(
            title="🌟 Crystal Hub Premium Control Panel",
            description="Welcome to your premium dashboard",
            color=0xFF69B4
        )

        # Server Statistics
        stats = f"📊 **Server Statistics**\n"
        stats += f"Members: {interaction.guild.member_count}\n"
        stats += f"Premium Users: {len([m for m in interaction.guild.members if premium_role in m.roles])}\n"
        embed.add_field(name="", value=stats, inline=False)

        # Quick Controls
        controls = "⚡ **Quick Controls**\n"
        controls += "🔒 - Lock all channels\n"
        controls += "🔓 - Unlock all channels\n"
        controls += "✅ - Toggle verification\n"
        controls += "⚡ - Boost mode"
        embed.add_field(name="", value=controls, inline=False)

        # Premium Features
        features = "💎 **Premium Features**\n"
        features += "• Advanced Analytics\n"
        features += "• Auto-moderation\n"
        features += "• Custom Commands\n"
        features += "• Priority Support"
        embed.add_field(name="", value=features, inline=False)

        # Create view with buttons
        class ControlButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @discord.ui.button(label="Lock", emoji="🔒", style=discord.ButtonStyle.gray, custom_id="lock")
            async def lock_button(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                await button_interaction.response.send_message("Channels locked!", ephemeral=True)

            @discord.ui.button(label="Unlock", emoji="🔓", style=discord.ButtonStyle.gray, custom_id="unlock")
            async def unlock_button(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                await button_interaction.response.send_message("Channels unlocked!", ephemeral=True)

            @discord.ui.button(label="Verify", emoji="✅", style=discord.ButtonStyle.gray, custom_id="verify")
            async def verify_button(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                await button_interaction.response.send_message("Verification toggled!", ephemeral=True)

            @discord.ui.button(label="Boost", emoji="⚡", style=discord.ButtonStyle.gray, custom_id="boost")
            async def boost_button(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                await button_interaction.response.send_message("Boost mode toggled!", ephemeral=True)

        await interaction.response.send_message(embed=embed, view=ControlButtons())

async def setup(bot):
    await bot.add_cog(ControlPanel(bot))