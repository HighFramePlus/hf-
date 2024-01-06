import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse

async def download_youtube_video(url: str):
    parsed_url = urlparse(url)

    if parsed_url.scheme and parsed_url.netloc:
        if parsed_url.netloc == "youtu.be":
            url = "https://www.youtube.com/watch?v=" + parsed_url.path.lstrip("/")

        vgm_url = "https://10downloader.com/download?v=" + url
        try:
            async with aiohttp.ClientSession() as session:
                html_text = await session.get(url=vgm_url)
                html_text = await html_text.read()
        except:
            return None, None, None

        soup = BeautifulSoup(html_text.decode('utf-8'), "html.parser")
        download = soup.find("tbody").find("a", href=True, text="Download")
        if not download:
            return None, None, None

        download_url = download["href"]
        thumbnail_url = soup.find("div", {"class": "info"}).find("img")["src"]
        video_title = soup.find("div", {"class": "info"}).find("span", {"class": "title"}).text.strip()

        link = "http://tinyurl.com/api-create.php?url=" + download_url
        try:
            async with aiohttp.ClientSession() as session:
                short_url = await session.get(url=link)
                short_url = await short_url.read()
        except:
            return None, None, None

        short_url = short_url.decode('utf-8')

        return video_title, thumbnail_url, short_url
    else:
        return None, None, None