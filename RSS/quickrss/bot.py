import discord
import feedparser
import os
import asyncio
from discord.ext import tasks, commands

# Load environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
RSS_FEED_URL = os.getenv('RSS_FEED_URL')
DISCORD_CHANNEL_IDS = os.getenv('DISCORD_CHANNEL_IDS').split(',')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to fetch the RSS feed
def fetch_rss_feed():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries

# Background task to check the RSS feed
@tasks.loop(minutes=10)
async def check_feed():
    latest_entries = fetch_rss_feed()
    with open('latest_entry.txt', 'r') as file:
        latest_entry_link = file.read().strip()

    new_entries = [entry for entry in latest_entries if entry.link != latest_entry_link]

    for entry in new_entries:
        for channel_id in DISCORD_CHANNEL_IDS:
            channel = bot.get_channel(int(channel_id))
            if channel is not None:
                await channel.send(f"New post: {entry.title}\n{entry.link}")

    if new_entries:
        with open('latest_entry.txt', 'w') as file:
            file.write(new_entries[0].link)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    check_feed.start()

# Command to manually check the RSS feed
@bot.command()
async def check(ctx):
    await ctx.send("Checking RSS feed...")
    await check_feed()

# Run the bot
bot.run(BOT_TOKEN)
