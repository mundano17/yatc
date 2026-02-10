import asyncio

import aiohttp

from src.services.scraper import Scraping
from src.services.validator import validate

urls = [
    "https://economictimes.indiatimes.com/industry/energy/oil-gas/putins-war-chest-drained-by-big-discounts-that-keep-oil-flowing/articleshow/128167779.cms"
]


async def Crawler(urls: list[str], userAgent: str = "*"):
    async with aiohttp.ClientSession() as session:
        tasks = [validate(session, i, userAgent) for i in urls]
        allowed_links = [link for link in await asyncio.gather(*tasks) if link]
        scraped = await asyncio.gather(
            *[(Scraping(session, link, userAgent)) for link in allowed_links]
        )
    print(scraped)
    return scraped


asyncio.run(Crawler(urls))
