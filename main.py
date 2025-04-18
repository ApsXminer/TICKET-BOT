import discord
import json
import os
import time
from colorama import init, Fore, Style
from discord.ext import commands, tasks
from cogs.ticket_system import Ticket_System
from cogs.ticket_commands import Ticket_Command

# Initialize colorama
init(autoreset=True, convert=True)

RED = Fore.RED
BLUE = Fore.BLUE
RESET = Style.RESET_ALL

def print_banner():
    banner = f"""{RED}
   ██████╗ ██████╗ ██████╗ ███████╗    ██╗  ██╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚██╗██╔╝
  ██║     ██║   ██║██║  ██║█████╗       ╚███╔╝ 
  ██║     ██║   ██║██║  ██║██╔══╝       ██╔██╗ 
  ╚██████╗╚██████╔╝██████╔╝███████╗    ██╔╝ ██╗
   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝
         {BLUE}CODEX - Ticket BOT {RESET}
 {BLUE} github.com/ApsXminer | discord.gg/3xzPkYHd9U {RESET}
"""
    lines = banner.splitlines()
    width = os.get_terminal_size().columns
    for line in lines:
        centered = line.center(width)
        for char in centered:
            print(char, end='', flush=True)
            time.sleep(0.001)
        print()

# Load config
with open("config.json", mode="r") as config_file:
    config = json.load(config_file)

BOT_TOKEN = config["token"]
GUILD_ID = config["guild_id"]
CATEGORY_ID1 = config["category_id_1"]
CATEGORY_ID2 = config["category_id_2"]

bot = commands.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print_banner()
    print(f'Bot Started | {bot.user.name}')
    richpresence.start()

@tasks.loop(minutes=1)
async def richpresence():
    guild = bot.get_guild(GUILD_ID)
    category1 = discord.utils.get(guild.categories, id=int(CATEGORY_ID1))
    category2 = discord.utils.get(guild.categories, id=int(CATEGORY_ID2))

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f'Tickets | {len(category1.channels) + len(category2.channels)}'
        )
    )

bot.add_cog(Ticket_System(bot))
bot.add_cog(Ticket_Command(bot))
bot.run(BOT_TOKEN)
