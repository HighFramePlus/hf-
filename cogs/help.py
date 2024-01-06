import discord
from discord.ext import commands

from core.embeds import create_embed, format_pagination_embeds, page
from discord.ext import menus  # Assuming you have this library for pagination
from utils.message import edit_or_reply
from utils.testing import can_use_limited_test_commands

# Replace the following constants with your actual values
DISCORD_INVITES = {"support": "https://discord.gg/example"}
DEFAULT_PREFIXES = ["!"]

# Replace the following functions with your actual implementations
def codeblock(language, lines):
    return f"```{language}\n" + "\n".join(lines) + "```"

def icon(name):
    # Replace with your implementation
    pass

def link(url, text):
    # Replace with your implementation
    pass

def pill(text):
    # Replace with your implementation
    pass

def small_pill(text):
    # Replace with your implementation
    pass

def icon_pill(name, text):
    # Replace with your implementation
    pass

def stringwrap(text, width):
    # Replace with your implementation
    pass

# Assuming you have a paginator implementation or use the one from the discord.ext library
class Paginator:
    @staticmethod
    async def create_paginator(ctx, pages):
        # Replace with your implementation or use discord.ext menus
        pass

# Your other functions and classes go here

# Replace your constants with actual values
categories = {
    "core": icon_pill("home", "Core Commands"),
    "info": icon_pill("information", "Information Commands"),
    "search": icon_pill("mag", "Search Commands"),
    "utils": icon_pill("tools", "Utility Commands"),
    "fun": icon_pill("stars", "Fun Commands"),
    "image": icon_pill("image", "Image Commands"),
    "mod": icon_pill("shield", "Moderation Commands")
}

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, args=None):
        if canUseLimitedTestCommands(ctx):
            categories["limited"] = f"{iconPill('stars', 'Limited Test Commands')}"
        elif "limited" in categories:
            del categories["limited"]

        if args:
            await ctx.trigger_typing()
            # Detailed command view
            result_scores = {}
            result_mappings = {}

            for c in ctx.bot.commands:
                if (
                    c.name.lower().find(args.lower()) != -1
                    or any(a.lower().find(args.lower()) != -1 for a in c.aliases)
                ):
                    if c.metadata.explicit and not ctx.channel.nsfw:
                        continue
                    if not categories[c.metadata.category] and not ctx.author.id == ctx.bot.owner_id:
                        continue
                    result_scores[c.name] = 1
                    result_mappings[c.name] = c

                # Boost exact matches to rank higher in the result list
                if c.name.lower() == args.lower():
                    result_scores[c.name] += 1
                if any(a.lower() == args.lower() for a in c.aliases):
                    result_scores[c.name] += 1

            results = []
            result_scores = dict(sorted(result_scores.items(), key=lambda item: item[1], reverse=True))
            for k in result_scores.keys():
                results.append(result_mappings[k])

            pages = []
            prefix = DEFAULT_PREFIXES[0]

            try:
                if len(results) == 0:
                    return await editOrReply(ctx, create_embed("warning", ctx, "No commands found for the provided query."))

                if len(results) > 1:
                    # Command overview
                    cmds = [m.name for m in results]
                    dscs = [m.metadata.description_short for m in results]
                    pages.append(
                        page(
                            create_embed(
                                "default",
                                ctx,
                                {
                                    "description": f"Check the pages for full command details.\n\n"
                                    + render_command_list(cmds, dscs, 15)
                                    + f"\n\n{icon('question')} Need help with something else? Contact us via our {link(DISCORD_INVITES['support'], 'Support Server')}."
                                },
                            )
                        )
                    )

                    # Generate command detail pages
                    for c in results:
                        pages.append(create_command_page(ctx, prefix, c))

                    await paginator.createPaginator(
                        {
                            "context": ctx,
                            "pages": format_pagination_embeds(pages),
                        }
                    )
                    return
                else:
                    return await editOrReply(ctx, create_command_page(ctx, prefix, results[0]))
            except Exception as e:
                print(e)
        else:
            # Full command list
            commands_dict = {}
            descriptions_dict = {}

            for c in ctx.bot.commands:
                if not categories[c.metadata.category]:
                    continue
                if c.metadata.explicit and not ctx.channel.nsfw:
                    continue
                if not commands_dict[c.metadata.category]:
                    commands_dict[c.metadata.category] = []
                if not descriptions_dict[c.metadata.category]:
                    descriptions_dict[c.metadata.category] = []
                commands_dict[c.metadata.category].append(f"{c.name}")
                descriptions_dict[c.metadata.category].append(f"{c.metadata.description_short}")

            pages = []
            for cat in categories.keys():
                pages.append(create_help_page(ctx, categories[cat], commands_dict[cat], descriptions_dict[cat]))

            await paginator.createPaginator(
                {
                    "context": ctx,
                    "pages": format_pagination_embeds(pages),
                }
            )

def setup(bot):
    bot.add_cog(Help(bot))
