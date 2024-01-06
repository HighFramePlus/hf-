import discord
from discord.ext import commands
from discord_together import DiscordTogether
from discord.gateway import DiscordWebSocket
import pomice

from core import status
import cfg

import glob
import re

TOKEN=cfg.TOKEN
VER="0.02.41p"

activity = discord.Activity(type=discord.ActivityType.listening, name="check @5xtech.jpeg")
bot = commands.Bot(command_prefix=",",
                   intents=discord.Intents().all(),
                   activity=activity)

async def start_nodes():
    pomice_instance = pomice.NodePool()
    await pomice_instance.create_node(
        bot=bot,
        host="hfplusapi.ct8.pl",
        port=25024,
        password="hfplus@lavalink",
        identifier="MAIN",
    )
    print(f"Node is ready!")

@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether(TOKEN)
    await start_nodes()
    await bot.load_extension("jishaku")

    for file in glob.iglob("cogs/*.py"):
        try:
            await bot.load_extension("cogs.{}".format(re.split(r"/|\\", file)[-1][:-3]))
        except Exception as e:
            print(f"Failed to load {file} \n{type(e).__name__}: {e}")

DiscordWebSocket.identify = status.identify
bot.run(TOKEN)