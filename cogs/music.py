import discord
from discord.ext import commands
import pomice

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
        await ctx.send(f"Joined the voice channel `{channel}`")

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

            # Check if results is a non-empty list
            if not results:
                print(f"Invalid results: {results}")
                raise commands.CommandError("Invalid results")

            first_track = results[0]
            print(f"Playing track: {first_track.title} - {first_track.uri}")

            # Play the track
            await player.play(track=first_track)
            await player.set_volume(volume=100)  # Adjust the volume as needed

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