import discord
from discord.ext import commands
from discord.gateway import DiscordWebSocket

import requests

from core import status
from core import embeds

VER="0.756.3p"
VER_CHECK="https://raw.githubusercontent.com/HighFramePlus/api/main/ver_check.txt"
NAME="HF+"
FULLNAME="High Frame Plus"

activity = discord.Activity(type=discord.ActivityType.listening, name="check @5xtech.jpeg")
bot = commands.Bot(command_prefix="$",
                   intents=discord.Intents().all(),
                   activity=activity)

MAX_LVL_ID = 1192592719340654703

def has_max_level():
    async def predicate(ctx):
        role = discord.utils.get(ctx.author.roles, id=MAX_LVL_ID)
        return role is not None
    return commands.check(predicate)

@bot.event
async def on_ready():
    await bot.load_extension('jishaku')

@bot.command(name="rickroll")
@has_max_level()
async def rrll(ctx):
    await ctx.send(f"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYHzp1ZE_xL3BbMSL8vOWcvyC1BN7VAoQEvWwhSyvMCg&s")

@rrll.error
async def restricted_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"<:nerd:1192924888009293854> **Rlly? you can`t use this command yet!**\nGet level 50 role **[**<@&{MAX_LVL_ID}>**]** to get access to this command")

DiscordWebSocket.identify = status.identify
bot.run("MTE5Mjg5NTUwODAyNTQ2Mjk2Ng.Gz5-se.06F6YuFM7Mi1Ui2OLm1BsMqBrZ53EPzAdx_98U")