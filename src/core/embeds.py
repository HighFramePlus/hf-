import discord

def debug_embed(title_str, desc_str): 
    return discord.Embed(
        title=title_str or "No title specifed",
        description=desc_str or "No description specifed"
    )