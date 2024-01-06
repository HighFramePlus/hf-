import discord
from discord.ext import commands
import datetime
import time
import psutil
import asyncio
import random

def format_date(dt: datetime.datetime):
    if dt is None:
        return 'N/A'
    return f'<t:{int(dt.timestamp())}>'

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(aliases=['stats'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def about(self, ctx):
        total_members = 0
        total_unique = len(self.bot.users)

        text = 0
        voice = 0
        guilds = 0

        for guild in self.bot.guilds:
            guilds += 1
            if guild.unavailable:
                continue

            total_members += guild.member_count or 0
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1

                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        dpy_version = discord.__version__
        dev = self.bot.get_user(710247495334232164)

        em = discord.Embed(color=0xffffff)
        if dev and dev.avatar is not None:
            em.set_author(name=dev, icon_url=dev.avatar.url)

        em.title = "About"
        em.description = self.bot.description

        em.add_field(
            name="Users",
            value=f"{total_members} total\n{total_unique} unique"
        )

        em.add_field(
            name="Channels",
            value=f"{text + voice} total\n{text} text\n{voice} voice"
        )

        em.add_field(
            name="Process",
            value=f"{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU"
        )

        em.add_field(
            name="Guilds",
            value=guilds
        )

        em.add_field(
            name="Discord.py version",
            value=dpy_version
        )

        if self.bot.user and self.bot.user.avatar is not None:
            em.set_thumbnail(url=self.bot.user.avatar.url)
        em.set_footer(text="Made with 💖 with discord.py", icon_url="http://i.imgur.com/5BFecvA.png")

        await ctx.send(embed=em)

    @commands.command(aliases=['latency'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        time1 = time.perf_counter()
        msg = await ctx.send("Pinging...")
        time2 = time.perf_counter()

        await msg.edit(content=
            "🏓 Pong!"
            f"\nAPI: `{round(self.bot.latency*1000)}ms`"
            f"\nBot: `{round(time2-time1)*1000}ms`"
        )

    @commands.command(aliases=['si'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        def formatted_date(date):
            if date is None:
                return 'N/A'
            return f'{date:%m-%d-%Y | %H:%M} UTC'


        if ctx.guild is not None:
            features = [f.lower().title().replace("_", " ") for f in ctx.guild.features]
            all_features = f" " + f"\n ".join(features)

            boost_level = f"{ctx.guild.premium_tier} Level" if {ctx.guild.premium_tier} == 2 else "No Level"
            boosts = f"<:booster:983684380134371339> {ctx.guild.premium_subscription_count} Boosts ({boost_level})"

            em = discord.Embed(title=ctx.guild.name, color=0xffffff)
            if ctx.guild.owner is not None:
                em.description = f"""
    **Owner:** {ctx.guild.owner.mention} `[{ctx.guild.owner}]`
    **Description:** {ctx.guild.description if ctx.guild.description else "N/A"}
    **ID:** {ctx.guild.id}
    """

            em.add_field(
                name=f'👥 {ctx.guild.member_count} Members',
                value=(
                    f'<:memberlist:811747305543434260> Humans: {len([m for m in ctx.guild.members if not m.bot])}\n'
                    f'<:botlist:811747723434786859> Bots: {sum(member.bot for member in ctx.guild.members)}'
                ),
                inline=False
            )

            em.add_field(
                name='Channels',
                value=(
                    f'<:textchannel:811747767763992586> Text: {len(ctx.guild.text_channels)}\n'
                    f'<:voicechannel:811748732906635295> Voice: {len(ctx.guild.voice_channels)}\n'
                    f'📁 Categories: {len(ctx.guild.categories)}'
                ),
                inline=False
            )

            em.add_field(name='<:role:985140259702583326> Role Count', value=len(ctx.guild.roles), inline=False)
            em.add_field(name='🙂 Emoji Count', value=len(ctx.guild.emojis), inline=False)

            em.add_field(
                name='<:verified:985139472813412362> Verification level',
                value=str(ctx.guild.verification_level).capitalize(),
                inline=False
            )

            em.add_field(
                name="✨ Server Features",
                value=f"{boosts}\n" + all_features if boosts and features else f'{self.bot.no} None',
                inline=False
            )

            if ctx.guild.icon:
                em.set_thumbnail(url=ctx.guild.icon.url)

            else:
                em.set_thumbnail(url="https://logos-world.net/wp-content/uploads/2020/12/Discord-Logo.png")

            em.set_footer(text=f'Created at: {formatted_date(ctx.guild.created_at)}')
            
            await ctx.send(embed=em)

    @commands.command(aliases=["ss"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def screenshot(self, ctx, *, url: str):
        await ctx.send(f"https://image.thum.io/get/https://{url}")

    @commands.command()
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def hack(self, ctx, member: discord.Member):
        """Hack someone and get their details."""

        used_words = ['Nerd','Sucker','Noob','Sup','Yo','Wassup','Nab','Nub','fool','stupid']
        mails = ['@gmail.com','@hotmail.com','@yahoo.com']

        if member is ctx.author:
            return await ctx.send("You can't hack yourself.")
        else:
            hacking = await ctx.send(f"Hacking {member.name}....")
            await asyncio.sleep(1.55)
            await hacking.edit(content='Finding info....')
            await asyncio.sleep(1.55)
            await hacking.edit(content=f"Discord email address: {member.name}{random.choice(mails)}")
            await asyncio.sleep(2)
            await hacking.edit(content=f"Password: x2yz{member.name}xxy65{member.discriminator}")
            await asyncio.sleep(2)
            await hacking.edit(content=f'Most used words: {random.choice(used_words)}')
            await asyncio.sleep(1.55)
            await hacking.edit(content='IP address: 127.0.0.1:50')
            await asyncio.sleep(1.55)
            await hacking.edit(content='Selling information to the government....')
            await asyncio.sleep(2)
            await hacking.edit(content=f'Reporting {member.name} to Discord for violating ToS')
            await asyncio.sleep(2)
            await hacking.edit(content='Hacking medical records.....')
            await asyncio.sleep(1.55)
            await hacking.edit(content=f"{ctx.author.mention} successfully hacked {member.mention}")

            await ctx.send("The ultimate, totally real hacking has been completed!")

async def setup(bot):
    await bot.add_cog(Utility(bot))
