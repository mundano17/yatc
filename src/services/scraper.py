import aiohttp
from bs4 import BeautifulSoup
from readability import Document

from src.models.scraper import Scrape


async def Scraping(
    session: aiohttp.ClientSession, link: str, userAgent: str = "*"
) -> Scrape:
    try:
        header = {"User-Agent": userAgent}
        async with session.get(
            link, headers=header, timeout=aiohttp.ClientTimeout(5)
        ) as res:
            doc = Document(await res.text())
            if res.status != 200:
                raise ValueError(f"HTML Error: {res.status}")
            if len(doc.content() or "") > 30:
                soup = BeautifulSoup(doc.summary(), "html.parser")
                return Scrape(text=soup.get_text(separator="\n", strip=True), url=link)
            else:
                raise ValueError("len of scraped content is insufficient")
    except aiohttp.ClientError as e:
        print("Scraping error:", e)
        return Scrape(text="", url=link)
