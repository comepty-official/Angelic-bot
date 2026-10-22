import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Angelic Bot is online as {bot.user}!")
    
    # Force a global sync so the commands work in DMs and other servers
    await bot.tree.sync()
    print("🔄 Angelic commands synced globally!")

async def load_cogs():
    for item in os.listdir('./cogs'):
        if item.endswith('.py'):
            await bot.load_extension(f'cogs.{item[:-3]}')
            print(f"✅ Loaded {item}")

@bot.event
async def setup_hook():
    await load_cogs()

bot.run(os.getenv("DISCORD_TOKEN"))