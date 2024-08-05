import discord
import feedparser
import asyncio
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)

RSS_FEED_URL = 'https://example.com/rss'
DISCORD_CHANNEL_ID = 123456789012345678  # Replace with your channel ID
CHECK_INTERVAL = 60 * 60  # Check every hour

last_published = None

async def fetch_rss():
    global last_published
    feed = feedparser.parse(RSS_FEED_URL)
    if feed.entries:
        latest_entry = feed.entries[0]
        if last_published is None or latest_entry.published_parsed > last_published:
            last_published = latest_entry.published_parsed
            return latest_entry
    return None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.wait_until_ready()
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    while not client.is_closed():
        entry = await fetch_rss()
        if entry:
            await channel.send(f"New post: {entry.title}\n{entry.link}")
        await asyncio.sleep(CHECK_INTERVAL)

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)
