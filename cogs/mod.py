import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sn'])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setnick(self, ctx, member: discord.Member, *, nick):
        try:
            await member.edit(nick=nick)
            await ctx.send(f'Nickname for {member.name} was changed to {member.mention}')
        
        except discord.HTTPException:
            await ctx.send("Something went wrong.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))