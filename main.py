import os
import discord
import argparse
from discord.ext import commands
from dotenv import load_dotenv
import sys

# load environment variables
load_dotenv()

# Parse CLI args (prod use)
parser = argparse.ArgumentParser()
parser.add_argument("--token", help="Discord bot token")
args = parser.parse_args()

TOKEN = args.token or os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ No token provided. Use --token or set DISCORD_TOKEN in .env")
    sys.exit(1)

# create bot
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is now ready to use")

    # dynamically load all slash commands (cogs)
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename}")

    # sync all slash commands
    await client.tree.sync()
    print("Slash commands are now synced")

# run bot
client.run(TOKEN)

