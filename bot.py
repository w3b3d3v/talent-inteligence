import datetime
import dateStore
import discord
from dotenv import load_dotenv
import os
from typing import List, Dict, Any
from model import Model
import strapi
from matcher import Matcher
from job_announce_checker import JobAnnounceChecker
from scripts.grantRole import grant_role_to_users
import requests

load_dotenv()

NAME = ["rafael", "lorenzo", "daniel", "ana", "anna", "melk"]
UF = ["rs", "rio grande do sul", "sp", "são paulo", "rj", "rio de janeiro"]
TECHS = ["angular", "linguagem c", "c#", "c++", "clojure", "dart", "elixir", "elm", "erlang", "f#", "ganache", "go", "graphql", "hardhat", "haskell", "java", "javascript", "kind", "kotlin", "meteor.js", "mongodb", "mysql", "nextjs", "node", "postgresql", "python", "react", "ruby", "rust", "scala", "solidity", "swift", "teal", "truffle", "typescript", "vue", "vyper"]
JOBS = ["founder", "engenheiro front end", "engenheiro back end", "engenheiro full stack", "engenheiro solidity", "engenheiro solana", "engenheiro full stack web3", "engenheiro de dados", "engenheiro de jogos", "devops", "product manager", "product designer", "ui/ux", "community manager", "marketing / growth", "devrel", "escritor técnico", "contribuinte de daos"]
CHANNEL_ID_TO_CHECK = "923218912613634049"
WEB3DEV_GUILD_ID = "898706705779687435"


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
    return matcher_results + result_model


async def processSingleMessage(message_content: str, author_id: str) -> List[Dict[str, Any]]:
    matcher = Matcher(jobs=JOBS, techs=TECHS, names=NAME, uf=UF)
    matched = matcher.match_prompt(prompt=message_content)
    if matched:
        formated = matcher.to_json(matches=matched)
        formated["discord_id"] = author_id
    else:
        formated = {}

    ai_prompts = matcher.get_ai_prompts()

    model = Model(prompts=ai_prompts, techs_list=TECHS, jobs_list=JOBS)
    predictions = model.extract_from_all_prompts()
    formated_preds = model.format_responses(responses=predictions)
    json_preds = model.to_json(responses=formated_preds)
    result_model = insert_discord_id_in_json(json_preds, [author_id])

    return [formated] + result_model


def insert_discord_id_in_json(json_preds: List, ids: List):
    json_preds_with_id = []
    for pred, user_id in zip(json_preds, ids):
        pred["discord_user_id"] = user_id
        json_preds_with_id.append(pred)

    return json_preds_with_id


def store_predictions(predictions: List):
    predictions = [pred for pred in predictions if pred]
    api = strapi.Api(predictions=predictions, jobs=JOBS, techs=TECHS)
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
    url = f"https://us-central1-web3dev-bootcamp.cloudfunctions.net/grantDiscordRoleToNewcomer?discordId={member.id}"
    headers = {}
    print(f'User {member.name} joined the server. Triggered cloud function.')
    res = requests.get(url=url, headers=headers)

    if res.status_code == 200:
        print("Granted roles to user successfully.")
    else:
        print("Error granting roles to user.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!model'):
        args = message.content.split(' ')
        if len(args) == 1:
            await message.channel.send('Essa mensagem não é um comando.')
            return

        command = args[1]
        if command == 'processAll':
            if len(args) != 5:
                await message.channel.send('Comando inválido. Use: `!model processAll <guild_id> <channel_id> <num_messages>`')
                return

            guild_id = args[2]
            channel_id = args[3]
            num_messages = int(args[4])

            try:
                guild = await client.fetch_guild(guild_id)
                channel = await guild.fetch_channel(channel_id)
            except (discord.HTTPException, discord.InvalidData, discord.NotFound):
                await message.channel.send('Não foi possível encontrar o servidor ou canal com os IDs fornecidos.')
                return

            last_date = dateStore.load_last_date()
            predictions = await processMessagesOnChannel(channel, num_messages, last_date)
            store_predictions(predictions=predictions)

        elif command == 'servers':
            server_count = len(client.guilds)
            server_names = '\n'.join(guild.name for guild in client.guilds)
            await message.channel.send(f'Estamos em {server_count} servidores:\n{server_names}')

        elif command == 'permissions':
            if len(args) != 3:
                await message.channel.send('Comando inválido. Use: `!model permissions <guild_id>`')
                return

            guild_id = args[2]

            try:
                guild = await client.fetch_guild(guild_id)
                me = await guild.fetch_member(client.user.id)
            except (discord.HTTPException, discord.InvalidData, discord.NotFound):
                await message.channel.send('Não foi possível encontrar o servidor com o ID fornecido.')
                return

            await message.channel.send(me.guild_permissions.text())

        elif command == 'grantRole':
            if len(args) != 3:
                await message.channel.send('Comando inválido. Use: `!model grantRole <role_id>`')
                return

            role_id = args[2]
            try:
                await grant_role_to_users(client=client, filename="users.csv", role_id=role_id)

            except Exception as e:
                print(e)
                await message.channel.send('Ocorreu um erro ao dar o cargo aos usuários. Tente novamente mais tarde.')
                return

    elif str(message.channel.id) == CHANNEL_ID_TO_CHECK:
        print("Received message from apresente-se. Processing...")
        try:
            predictions = await processSingleMessage(message_content=message.content, author_id=str(message.author.id))
            store_predictions(predictions=predictions)
        except Exception as e:
            print(e)
            await message.channel.send('Ocorreu um erro ao processar as mensagens. Tente novamente mais tarde.')
            return

    # else:
    #     is_job_announcement = check_job_announcement(message.content)
    #     if is_job_announcement:
    #         await message.reply('<@&1086370714354995342>')


client.run(os.getenv("BOT_TOKEN"))
