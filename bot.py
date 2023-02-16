
import discord
from dotenv import load_dotenv
import os
from typing import List
from matcher import Matcher

load_dotenv()
users = []
last_created_at = [None]

async def processMessagesOnChannel(channel: str, msg_limit: int) -> List[str]:
    data = []
    i = 1
    async for message in channel.history(limit=msg_limit, oldest_first=True, after=last_created_at[-1]):
        if i == msg_limit:
            last_created_at.append(message.created_at)
        data.append((message.content, message.author.id, message.author.name))
        i += 1
    
    matcher = Matcher()
    prompts = [message[0] for message in data]
    ids = [user_id[1] for user_id in data]
    names = [name[2] for name in data]

    for prompt, discord_id, name in zip(prompts, ids, names):
        new_user = matcher.build_user(prompt, name, discord_id)
        users.append(new_user)

async def process_message(prompt: str, name: str, discord_id: str) -> List[str]:
    matcher = Matcher()
    new_user = matcher.build_user(prompt, name, discord_id)
    return new_user

async def get_channel_by_id(channel_id: str):
    try:
        channel = await client.fetch_channel(channel_id)
        return channel
    except discord.errors.HTTPException:
        return

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
    if message.content.startswith('!matcher'):
        args = message.content.split(' ')
        if len(args) == 1:
            await message.channel.send('Essa mensagem não é um comando.')
            return
        if args[1] == 'processAll':
            channel = await get_channel_by_id(args[2])
            if not channel:
                await message.channel.send('Não consegui encontrar um canal com esse Id.')

            await processMessagesOnChannel(channel, int(args[3]))
    else:
        user = await process_message(message.content, message.author.name, message.author.id)

client.run(os.getenv("BOT_TOKEN"))


