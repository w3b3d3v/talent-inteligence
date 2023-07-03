import csv
from typing import List


def read_csv(filename: str) -> List:
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            return [row[1] for row in reader]

    except FileNotFoundError:
        print(f"File {filename} not found")
        return []

def check_user_in_discord(guild, user_id: str) -> bool:
    member = guild.get_member(int(user_id))
    return member

def get_web3dev_guild(client):
    web3dev_guild_id = 898706705779687435 
    return client.get_guild(web3dev_guild_id)

async def grant_role_to_users(client, filename: str, role_id: str):
    discord_ids = read_csv(filename)
    guild = get_web3dev_guild(client)
    role = guild.get_role(int(role_id))

    for discord_id in discord_ids:
        member = check_user_in_discord(guild, discord_id)
        if member:
            await member.add_roles(role)
            print(f"Granted role to user {discord_id} successfully.")
    return