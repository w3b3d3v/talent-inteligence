
import discord
from dotenv import load_dotenv
import os
from typing import List, Dict
from model import Model
from database import Database
from discord.ext import commands

load_dotenv()

async def processMessagesOnChannel(channel: str, msg_limit: int) -> List[str]:
    messages = [(message.content, message.author.id) async for message in channel.history(limit=msg_limit)]
    prompts = [message[0] for message in messages]
    ids = [message[1] for message in messages]
    model = Model(prompts=prompts)
    predictions = model.extract_from_all_prompts()
    formated_preds = model.format_responses(responses=predictions)
    return zip(ids, formated_preds)

def setup_database(db_file):
    db = Database(db_file=db_file)
    return db;

def store_predictions(db, predictions: List):
    conn = db.create_connection()
    db.create_predictions_table(conn)
    for user_id, prediction in predictions:
        print(user_id, prediction)
        db.insert_prediction(conn, (user_id, prediction[1]["job"], prediction[1]["techs"]))

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

            predictions = await processMessagesOnChannel(channel, int(args[4]))
        
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
            print(me.guild_permissions.text())
            
    else:
        print(message.content)


client.run(os.getenv("BOT_TOKEN"))


