import aiohttp
from bs4 import BeautifulSoup
from readability import Document


async def Scraping(session: aiohttp.ClientSession, link: str, userAgent: str = "*"):
    try:
        header = {"User-Agent": userAgent}
        async with session.get(
            link, headers=header, timeout=aiohttp.ClientTimeout(5)
        ) as res:
            doc = Document(await res.text())
            if len(doc.content() or "") > 30:
                soup = BeautifulSoup(doc.summary(), "html.parser")
                return soup.get_text(separator="\n", strip=True)
    except aiohttp.ClientError as e:
        print("Scraping error:", e)
        return None
