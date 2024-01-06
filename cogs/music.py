import discord
from discord.ext import commands
import pomice
from urllib.parse import urlparse, parse_qs

def get_youtube_video_id(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the video ID from the query parameters
    video_id = parse_qs(parsed_url.query).get('v', [None])[0]

    return video_id

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["connect"])
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            channel = getattr(ctx.author.voice, "channel", None)
            if not channel:
                raise commands.CheckFailure(
                    "You must be in a voice channel to use this command "
                    "without specifying the channel argument.",
                )

        await ctx.author.voice.channel.connect(cls=pomice.Player)
        return channel

    @commands.command(aliases=["dc", "disconnect"])
    async def leave(self, ctx):
        if not ctx.voice_client:
            raise commands.CommandError("No player detected")

        player: pomice.Player = ctx.voice_client
        await player.destroy()
        await ctx.send("Player has left the channel.")

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, search: str):
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        player: pomice.Player = ctx.voice_client

        try:
            results = await player.get_tracks(search)
            if not results:
                print(f"Invalid results: {results}")
                raise commands.CommandError("Invalid results")

            first_track = results[0]
            video_id = get_youtube_video_id(first_track.uri)

            embed = discord.Embed(
                type="rich",
                description=f"# <:i_:1193254871898525736>  **` Now Playing `**\n"
                            + f"<:i_:1193246591600033853>  **` Title         `** ` {first_track.title} `\n"
                            + f"<:i_:1193246596574486679>  **` YouTube Link  `** ` {first_track.uri} `\n"
                            + f" \n"
                            + f"<:i_:1193246595089702915> [**` Source Code  `**](https://github.com/HighFramePlus) ​ ​"
                            + f" <:i_:1193246592925442109> [**` Invite HF+  `**](https://discord.com/api/oauth2/authorize?client_id=1192895508025462966&permissions=8&scope=bot)",
                color=2829617
            )
            embed.set_footer(
                text=f"{self.bot.user.name}",
                icon_url=f"{self.bot.user.avatar}",
            )
            embed.set_thumbnail(
                url=f"https://i3.ytimg.com/vi/{video_id}/maxresdefault.jpg"
            )
            await ctx.send(embed=embed)

            await player.play(track=first_track)
            await player.set_volume(volume=100)

        except pomice.exceptions.TrackLoadError as e:
            print(f"Error loading the track: {e}")
            await ctx.send(f"Error loading the track. Please check if the video is available or try another one.")

    @commands.command(aliases=["s"])
    async def stop(self, ctx):
        if not ctx.voice_client:
            raise commands.CommandError("No player detected")

        player: pomice.Player = ctx.voice_client

        if not player.is_playing:
            return await ctx.send("Player is already stopped!")

        await player.stop()
        await ctx.send("Player has been stopped")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))