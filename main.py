import discord
from discord.ext import commands
from discord_together import DiscordTogether
from discord.gateway import DiscordWebSocket

from core import status

import glob
import re

activity = discord.Activity(type=discord.ActivityType.listening, name="check @5xtech.jpeg")
bot = commands.Bot(command_prefix=",",
                   intents=discord.Intents().all(),
                   activity=activity)

@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether("MTE5Mjg5NTUwODAyNTQ2Mjk2Ng.GR1wT0.CTS3uAGoucU-trvEyEFLnVs6hMSHU8mWVvDzgw")
    await bot.load_extension("jishaku")

    for file in glob.iglob("cogs/*.py"):
        try:
            await bot.load_extension("cogs.{}".format(re.split(r"/|\\", file)[-1][:-3]))
        except Exception as e:
            print(f"Failed to load {file} \n{type(e).__name__}: {e}")

DiscordWebSocket.identify = status.identify
bot.run("MTE5Mjg5NTUwODAyNTQ2Mjk2Ng.GR1wT0.CTS3uAGoucU-trvEyEFLnVs6hMSHU8mWVvDzgw")