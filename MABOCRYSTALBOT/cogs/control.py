import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import hashlib
from datetime import datetime
import os

class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dashboard', 'instance', 'crystal.db')

    @app_commands.command(name="controlpanel")
    async def controlpanel(self, interaction: discord.Interaction):
        premium_role = discord.utils.get(interaction.guild.roles, id=1343002193321791558)
        if premium_role not in interaction.user.roles:
            await interaction.response.send_message("❌ You need premium to use Crystal Hub!", ephemeral=True)
            return

        embed = discord.Embed(
            title="🎮 Crystal Hub",
            description="Welcome to your premium script hub!\n\n"
                      "**Available Commands:**\n"
                      "🔑 Get Script - Download latest script\n"
                      "📊 View Stats - Check your statistics\n"
                      "🔄 Reset HWID - Update your hardware ID\n\n"
                      "**Need Help?**\n"
                      "• Support: <#support>\n"
                      "• Updates: <#announcements>\n"
                      "• Reviews: Use `/review`",
            color=0xFF69B4
        )

        class ScriptButtons(discord.ui.View):
            def __init__(self, cog):
                super().__init__()
                self.cog = cog

            @discord.ui.button(label="Get Script", emoji="🔑", style=discord.ButtonStyle.primary)
            async def get_script(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                try:
                    hwid = hashlib.sha256(f"crystal_hub_{button_interaction.user.id}".encode()).hexdigest()[:32]
                    conn = sqlite3.connect(self.cog.db_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT content FROM script ORDER BY id DESC LIMIT 1')
                    result = cursor.fetchone()
                    
                    if result:
                        script = result[0]
                        final_script = f"_G.HWID = '{hwid}'\n{script}"
                        try:
                            await button_interaction.user.send(f"```lua\n{final_script}\n```")
                            await button_interaction.response.send_message("✅ Script sent to your DMs!", ephemeral=True)
                            cursor.execute('UPDATE stats SET total_executions = total_executions + 1')
                            conn.commit()
                        except:
                            await button_interaction.response.send_message("❌ Enable DMs from server members!", ephemeral=True)
                    else:
                        await button_interaction.response.send_message("❌ No scripts available!", ephemeral=True)
                finally:
                    if 'conn' in locals():
                        conn.close()

            @discord.ui.button(label="View Stats", emoji="📊", style=discord.ButtonStyle.secondary)
            async def view_stats(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                try:
                    conn = sqlite3.connect(self.cog.db_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT total_executions FROM stats WHERE user_id = ?', (button_interaction.user.id,))
                    stats = cursor.fetchone()
                    executions = stats[0] if stats else 0
                    await button_interaction.response.send_message(f"📊 Your executions: {executions}", ephemeral=True)
                finally:
                    if 'conn' in locals():
                        conn.close()

            @discord.ui.button(label="Reset HWID", emoji="🔄", style=discord.ButtonStyle.danger)
            async def reset_hwid(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                new_hwid = hashlib.sha256(f"crystal_hub_{button_interaction.user.id}_{datetime.now()}".encode()).hexdigest()[:32]
                await button_interaction.response.send_message(f"✅ New HWID: `{new_hwid}`", ephemeral=True)

        await interaction.response.send_message(embed=embed, view=ScriptButtons(self))

async def setup(bot):
    await bot.add_cog(ControlPanel(bot))