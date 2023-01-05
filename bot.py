
import discord
from dotenv import load_dotenv
import os
from typing import List, Dict
from model import Model
from database import Database

load_dotenv()

async def processMessagesOnChannel(channel: str, msg_limit: int) -> List[str]:
    messages = [(message.content, message.author.id) async for message in channel.history(limit=msg_limit)]
    prompts = [message[0] for message in messages]
    ids = [message[1] for message in messages]
    model = Model(prompts=prompts)
    predictions = model.predict_all()
    return zip(ids, predictions)

def setup_database(db_file):
    db = Database(db_file=db_file)
    return db;

def store_predictions(db, predictions: List):
    conn = db.create_connection()
    db.create_predictions_table(conn)
    for user_id, prediction in predictions:
        print(user_id, prediction)
        db.insert_prediction(conn, (user_id, prediction[1]["job"], prediction[1]["techs"]))

async def process_message(content: str) -> List[str]:
    model = Model(prompts=content)
    predictions = model.predict_all()
    return predictions

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
    if message.content.startswith('!model'):
        args = message.content.split(' ')
        if len(args) == 1:
            await message.channel.send('Essa mensagem não é um comando.')
            return
        if args[1] == 'processAll':
            channel = await get_channel_by_id(args[2])
            if not channel:
                await message.channel.send('Não consegui encontrar um canal com esse Id.')

            predictions = await processMessagesOnChannel(channel, int(args[3]))

            db = setup_database("predictions.sqlite")
            store_predictions(db, predictions)
    else:
        print(f'processing message {message.id} on channel {message.channel.id}')
        preds = await process_message([message.content])
        print(preds)
        

client.run(os.getenv("BOT_TOKEN"))


