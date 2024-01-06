from collections import namedtuple

# Constants
class COLORS:
    embed = 0x00FF00  # Replace with the actual color code
    success = 0x00FF00  # Replace with the actual color code
    warning = 0xFFFF00  # Replace with the actual color code
    error = 0xFF0000  # Replace with the actual color code
    nsfw = 0xFFA500  # Replace with the actual color code

class STATIC_ICONS:
    warning = "warning_icon_url"  # Replace with the actual URL
    error = "error_icon_url"  # Replace with the actual URL
    adult = "adult_icon_url"  # Replace with the actual URL
    loading = "loading_icon_url"  # Replace with the actual URL
    ai = "ai_icon_url"  # Replace with the actual URL

class STATICS:
    labscore = "labscore_icon_url"  # Replace with the actual URL

class STATIC_ASSETS:
    chat_loading = "chat_loading_url"  # Replace with the actual URL

class SUPPORT_ARTICLES:
    AGE_RESTRICTED_CHANNELS = "age_restricted_channels_article"  # Replace with the actual article ID

# Named tuple to represent context
Context = namedtuple("Context", ["application"])

# Embed Types
def default(context):
    return {
        "color": COLORS.embed,
        "footer": {
            "iconUrl": STATICS.labscore,
            "text": context.application.name
        }
    }

def image(context):
    return {
        "color": COLORS.embed,
        "footer": {
            "iconUrl": STATICS.labscore,
            "text": context.application.name
        }
    }

def default_no_footer(context):
    return {
        "color": COLORS.embed
    }

def success(context):
    return {
        "author": {
            "name": "Success"
        },
        "color": COLORS.success
    }

def warning(context):
    return {
        "author": {
            "iconUrl": STATIC_ICONS.warning,
            "name": "Warning"
        },
        "color": COLORS.warning
    }

def error(context):
    return {
        "author": {
            "iconUrl": STATIC_ICONS.error,
            "name": "Error"
        },
        "color": COLORS.error
    }

def errordetail(context):
    return {
        "author": {
            "iconUrl": STATIC_ICONS.error,
            "name": "Error"
        },
        "color": COLORS.error
    }

def nsfw(context):
    return {
        "author": {
            "iconUrl": STATIC_ICONS.adult,
            "name": "This command is only available in Age Restricted channels.",
            "url": f"https://support.discord.com/hc/en-us/articles/{SUPPORT_ARTICLES.AGE_RESTRICTED_CHANNELS}"
        },
        "color": COLORS.nsfw
    }

def loading(context):
    return {
        "author": {
            "iconUrl": STATIC_ICONS.loading,
            "name": "Loading"
        },
        "color": COLORS.embed
    }

def ai(context):
    return {
        "author": {
            "iconUrl": STATIC_ICONS.ai,
            "name": "Generating"
        },
        "color": COLORS.embed
    }

def ai_custom(context):
    return {
        "author": {
            "iconUrl": STATIC_ICONS.ai,
            "name": ""
        },
        "image": {
            "url": STATIC_ASSETS.chat_loading
        },
        "color": COLORS.embed
    }

# Embed Types Mapping
embed_types = {
    "default": default,
    "image": image,
    "defaultNoFooter": default_no_footer,
    "success": success,
    "warning": warning,
    "error": error,
    "errordetail": errordetail,
    "nsfw": nsfw,
    "loading": loading,
    "ai": ai,
    "ai_custom": ai_custom,
}

# Create Embed
def create_embed(embed_type, context, content):
    if embed_type not in embed_types:
        raise ValueError("Invalid Embed Type")

    if not content:
        embed_types[embed_type](context)

    emb = embed_types[embed_type](context)

    if embed_type in ["success", "warning", "error", "loading", "ai"]:
        emb["author"]["name"] = content
        return emb

    if embed_type in ["ai_custom"]:
        emb["author"]["iconUrl"] = content

    if embed_type in ["errordetail"]:
        emb["author"]["name"] = content["error"]
        emb["description"] = content["content"]
        return emb

    if content and content["footer"] and not content["footer"]["iconUrl"] and embed_type != "defaultNoFooter":
        content["footer"]["iconUrl"] = STATICS.labscore

    if embed_type in ["image"]:
        if "://" in content["url"]:
            emb["image"] = {"url": content["url"]}
        else:
            emb["image"] = {"url": f"attachment://{content['url']}"}

        if content["provider"]:
            if content["provider"]["text"]:
                emb["footer"]["text"] = f"{content['provider']['text']} • {context.application.name}"
            if content["provider"]["icon"]:
                emb["footer"]["iconUrl"] = content["provider"]["icon"]

        if content["description"]:
            emb["description"] = content["description"]

        if content["time"] and emb["footer"]:
            emb["footer"]["text"] = f"{emb['footer']['text']} • Took {content['time']}s"

        return emb

    return {**emb, **content}

# Format Pagination Embeds
def format_pagination_embeds(embeds):
    if len(embeds) == 1:
        return embeds

    i = 0
    l = len(embeds)
    formatted = []
    for e in embeds:
        i += 1
        ne = e
        if not e:
            continue
        if e.get("embed"):
            ne["embed"]["footer"]["text"] = f"{e['embed']['footer']['text']} • Page {i}/{l}"
            formatted.append(ne)
        elif e.get("embeds"):
            ne["embeds"] = [se.update({"footer": {"text": f"{se['footer']['text']} • Page {i}/{l}"}}) for se in e["embeds"]]
            formatted.append(ne)
        else:
            formatted.append(e)
    return formatted

# Create Page
def page(embed):
    return {"embeds": [embed]}
