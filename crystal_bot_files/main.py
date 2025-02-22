import discord
from discord.ext import commands
import random
import datetime
import os

KEY_LOG_CHANNEL_ID = 1340825360769613834
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.content.startswith('!getkey'):
        user = message.author
        key = f'CRYSTAL-{random.randint(100000, 999999)}'
        
        try:
            user_embed = discord.Embed(
                title='Crystal Hub Key',
                description=f'Here\'s your key: `{key}`',
                color=discord.Color.green()
            )
            await user.send(embed=user_embed)
            
            channel = bot.get_channel(KEY_LOG_CHANNEL_ID)
            if channel:
                log_embed = discord.Embed(
                    title='New Key Generated',
                    description=f'User: {user.mention}\nKey: `{key}`',
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now()
                )
                log_embed.set_footer(text=f'User ID: {user.id}')
                await channel.send(f'🔑 New key generated for {user.mention}', embed=log_embed)

        except Exception as e:
            print(f'Error: {e}')
            await message.channel.send("Couldn't send DM. Please make sure your DMs are open.")

bot.run('MTM0MDYzNjA0NDg3MzMwMjA0Nw.GKlfNf.HXKSGLgQcLxDlmCM8DJGMjIJEaEEi8HMTE1fe0')