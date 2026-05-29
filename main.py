import discord
import re
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ROLE_NAME = "Owl"

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True          

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if re.search(r'\bwho\b', message.content, re.IGNORECASE):
        guild = message.guild
        role = discord.utils.get(guild.roles, name=ROLE_NAME)

        if not role:
            return
        if role in message.author.roles:
            return
        for member in role.members:
            await member.remove_roles(role)        
        await message.author.add_roles(role)
        response = f"Who who who, the Owl Hunter has found the new owl! It's {message.author.mention}!"
        await message.channel.send(response)

client.run(TOKEN)