import discord
from discord.ext import commands

import os

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="tv")
    async def tv(self, ctx):
        pass

    @tv.command()
    async def off(self, ctx):
        os.popen("echo 'off 0.0.0.0' | cec-client -s -d 1")

async def setup(bot):
    await bot.add_cog(Owner(bot))