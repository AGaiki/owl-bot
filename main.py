import discord
import re
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ROLE_NAME = "Owl"
DATA_FILE = "owl_data.json"

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True          

client = discord.Client(intents=intents)

def get_last_owl_time():
    """Reads the last assignment time, handling empty or missing files."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return None
        
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return datetime.fromisoformat(data['timestamp'])
    except (json.JSONDecodeError, KeyError):
        # If the file is garbled or missing the key, treat it as None
        return None

def save_owl_time():
    """Saves the current time, ensuring the file is created correctly."""
    now = datetime.now()
    with open(DATA_FILE, 'w') as f:
        json.dump({'timestamp': now.isoformat()}, f)
    return now

def format_duration(td):
    """Formats a timedelta into days, hours, and minutes."""
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    parts = []
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0: parts.append(f"{minutes}m")
    
    return ", ".join(parts) if parts else "less than a minute"

@client.event
async def on_ready():
    print(f'Owl Hunter is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if re.search(r'\bwho\b', message.content, re.IGNORECASE):
        guild = message.guild
        role = discord.utils.get(guild.roles, name=ROLE_NAME)

        if not role or role in message.author.roles:
            return

        # 1. Calculate time since last assignment
        last_time = get_last_owl_time()
        now = datetime.now()
        duration_str = ""
        
        if last_time:
            duration = now - last_time
            duration_str = f" The previous Owl held the perch for **{format_duration(duration)}**."

        # 2. Role Swap Logic
        for member in role.members:
            await member.remove_roles(role)
        
        await message.author.add_roles(role)
        
        # 3. Update the persistent timestamp
        save_owl_time()

        # 4. Send the announcement
        response = f"Who who who, the Owl Hunter has found the new owl! {message.author.mention}! {duration_str}"
        await message.channel.send(response)

client.run(TOKEN)