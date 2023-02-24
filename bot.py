import datetime
import dateStore
import discord
from dotenv import load_dotenv
import os
from typing import List
from model import Model
import strapi

load_dotenv()

async def processMessagesOnChannel(channel: str, msg_limit: int, after: datetime.datetime = None) -> List[str]:
    messages = [(message.content, message.author.id, message.created_at) async for message in channel.history(limit=msg_limit, oldest_first=True, after=after)]

    prompts = [message[0] for message in messages]
    ids = [message[1] for message in messages]
    last_created_at = dateStore.LastDate(messages[-1][-1])

    dateStore.save_last_date(last_created_at.last_date)

    model = Model(prompts=prompts)
    predictions = model.extract_from_all_prompts()
    formated_preds = model.format_responses(responses=predictions)
    json_preds = model.to_json(formated_preds)
    result = insert_discord_id_in_json(json_preds, ids)
    return result
    
def insert_discord_id_in_json(json_preds: List, ids: List):
    json_preds_with_id = []
    for pred, user_id in zip(json_preds, ids):
        pred["discord_user_id"] = user_id
        json_preds_with_id.append(pred)

    return json_preds_with_id

def store_predictions(predictions: List):
    api = strapi.Api(predictions=predictions)
    api.insert_predictions()

async def get_channel_by_id(channel_id: str):
    try:
        channel = await client.fetch_channel(channel_id)
        return channel
    except discord.errors.HTTPException:
        return

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!model'):
        args = message.content.split(' ')
        if len(args) == 1:
            await message.channel.send('Essa mensagem não é um comando.')
            return
        if args[1] == 'processAll':
            guild = await client.fetch_guild(args[2])
            channel = await guild.fetch_channel(args[3])

            if not channel:
                await message.channel.send('Não consegui encontrar um canal com esse Id.')
                return

            last_date = dateStore.load_last_date()
            predictions = await processMessagesOnChannel(channel, int(args[4]), last_date)
            store_predictions(predictions=predictions)
        
        elif args[1] == 'servers':
            await message.channel.send(f'Estamos em {len(client.guilds)} servidores')
            msg_str = ''
            for guild in client.guilds:
                msg_str += f'{guild.name}\n'
            await message.channel.send(msg_str)
        
        elif args[1] == 'permissions':
            guild = await client.fetch_guild(args[2])
            print(guild)
            me = await guild.fetch_member(str(977251314641801226))
            await message.channel.send(me.guild_permissions.text())
            
    else:
        pass


client.run(os.getenv("BOT_TOKEN"))


