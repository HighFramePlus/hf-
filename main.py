import discord
from discord.ext import commands
from discord_together import DiscordTogether
from discord.gateway import DiscordWebSocket
import pomice

from core import status
import config

import glob
import re

TOKEN=config.TOKEN
VER=config.VER

activity = discord.Activity(type=discord.ActivityType.listening,
                            name="hf.help ​ • ​ HF+")
bot = commands.Bot(command_prefix="hf.",
                   intents=discord.Intents().all(),
                   activity=activity,
                   help_command=None)

async def start_nodes():
    pomice_instance = pomice.NodePool()
    await pomice_instance.create_node(
        bot=bot,
        host="hfplusapi.ct8.pl",
        port=25024,
        password="hfplus@lavalink",
        identifier="MAIN",
    )
    print("Connected!")

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

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        type="rich",
        description="<:i_:1193246587967774730>  **` Core Commands  `**\n\n"
                    " ​ ​ ` help      ` ​ ​ ​ ​ ​Show full command list\n"
                    " ​ ​ ` ping      ` ​ ​ ​ ​ ​Bot connection details\n"
                    " \n"
                    "Use   ` hf.help <command> ` to view more information about a command.",
        color=2829617
    )
    embed.set_footer(
        text="HF+ • Page 1/7",
        icon_url=f"{bot.user.avatar}",
    )

    await ctx.send(embed=embed)

DiscordWebSocket.identify = status.identify
bot.run(TOKEN)