import discord
from discord.ext import commands
import os

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['test'])
    async def test(self, ctx):
        print("Test")

async def setup(bot):
    await bot.add_cog(Owner(bot))