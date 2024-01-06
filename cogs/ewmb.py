import discord
from discord.ext import commands

from core.embeds import create_embed, format_pagination_embeds, page, Context

class Embedderr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def example_embed(self, ctx):
        # Example command that uses the create_embed function
        embed_type = "success"  # Replace with the desired embed type
        content = "This is a success message!"  # Replace with the content of your message

        # Create the embed using the provided functions
        embed = create_embed(embed_type, ctx, content)

        # Send the embed
        await ctx.send(embed=discord.Embed.from_dict(embed))

    @commands.command()
    async def example_pagination(self, ctx):
        # Example command that uses the format_pagination_embeds and page functions
        embeds = []

        # Replace with actual values for each page
        page1_content = "Page 1 content"
        page2_content = "Page 2 content"

        embed_type = "default"  # Replace with the desired embed type

        # Create the embeds for each page
        page1_embed = create_embed(embed_type, ctx, page1_content)
        page2_embed = create_embed(embed_type, ctx, page2_content)

        # Add each page to the embeds list
        embeds.append(page(page1_embed))
        embeds.append(page(page2_embed))

        # Format the embeds for pagination
        formatted_embeds = format_pagination_embeds(embeds)

        # Send the formatted embeds
        for formatted_embed in formatted_embeds:
            await ctx.send(embed=discord.Embed.from_dict(formatted_embed["embed"]))

async def setup(bot):
    await bot.add_cog(Embedderr(bot))
