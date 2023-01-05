
import discord
from dotenv import load_dotenv
import os
from typing import List
from model import Model
from database import Database

load_dotenv()

async def processMessagesOnChannel(discord_channel_id: str, msg_limit: int) -> List[str]:
    channel = await client.fetch_channel(discord_channel_id)
    messages = [message.content async for message in channel.history(limit=msg_limit)]
    model = Model(prompts=messages)
    predictions = model.predict_all()
    return predictions

def setup_database(db_file):
    db = Database(db_file=db_file)
    return db;

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    predictions = await processMessagesOnChannel(message.content, 1)
    await message.channel.send(predictions)

client.run(os.getenv("BOT_TOKEN"))


