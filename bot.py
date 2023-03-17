import datetime
import dateStore
import discord
from dotenv import load_dotenv
import os
from typing import List
from model import Model
import strapi
from matcher import Matcher
from job_announce_checker import JobAnnounceChecker
import requests
import json

load_dotenv()

NAME = ["rafael", "lorenzo", "daniel", "ana", "anna", "melk"]
UF = ["rs", "rio grande do sul", "sp", "são paulo", "rj", "rio de janeiro"]
TECHS = ["angular", "linguagem c", "c#", "c++", "clojure", "dart", "elixir", "elm", "erlang", "f#", "ganache", "go", "graphql", "hardhat", "haskell", "java", "javascript", "kind", "kotlin", "meteor.js", "mongodb", "mysql", "nextjs", "node", "postgresql", "python", "react", "ruby", "rust", "scala", "solidity", "swift", "teal", "truffle", "typescript", "vue", "vyper"]
JOBS = ["founder", "engenheiro front end", "engenheiro back end", "engenheiro full stack", "engenheiro solidity", "engenheiro solana", "engenheiro full stack web3", "engenheiro de dados", "engenheiro de jogos", "devops", "product manager", "product designer", "ui/ux", "community manager", "marketing / growth", "devrel", "escritor técnico", "contribuinte de daos"]

async def processMessagesOnChannel(channel: str, msg_limit: int, after: datetime.datetime = None) -> List[str]:
    messages = [(message.content, message.author.id, message.created_at) async for message in channel.history(limit=msg_limit, oldest_first=True, after=after)]

    prompts = [message[0] for message in messages]
    ids = [message[1] for message in messages]
    last_created_at = dateStore.LastDate(messages[-1][-1])

    matcher = Matcher(jobs=JOBS, techs=TECHS, names=NAME, uf=UF)
    matcher_results = []
    for prompt, user_id in zip(prompts, ids):
        matched = matcher.match_prompt(prompt=prompt)
        if not matched:
            continue
        formated = matcher.to_json(matches=matched)
        formated["discord_id"] = user_id
        matcher.last_id_index = ids.index(user_id)
        matcher_results.append(formated)
    
    ai_prompts = matcher.get_ai_prompts()
    dateStore.save_last_date(last_created_at.last_date)

    model = Model(prompts=ai_prompts, techs_list=TECHS, jobs_list=JOBS)
    predictions = model.extract_from_all_prompts()
    formated_preds = model.format_responses(responses=predictions)
    json_preds = model.to_json(formated_preds)
    result_model = insert_discord_id_in_json(json_preds, ids[matcher.last_id_index:])
    return result_model + matcher_results
    
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

def check_job_announcement(message: str):
    job_checker = JobAnnounceChecker()
    is_job = job_checker.check_message(message=message)
    return is_job
    
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_member_join(member):
    url = None
    headers = None
    user_obj = {
        "discordId": member.id,
        "name": member.name,
        "joined_at": member.joined_at,
    }
    requests.post(url=url, headers=headers, json=json.dumps(user_obj))

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
            me = await guild.fetch_member(str(977251314641801226))
            await message.channel.send(me.guild_permissions.text())
            
    else:
        is_job_announcement = check_job_announcement(message=message.content)
        if(is_job_announcement):
            await message.reply('<@&1086370714354995342>')


client.run(os.getenv("BOT_TOKEN"))


