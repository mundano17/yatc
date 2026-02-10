import asyncio

import aiohttp

from src.services.scraper import Scraping
from src.services.validator import validate


async def Crawler(urls: list[str], userAgent: str = "*"):
    async with aiohttp.ClientSession() as session:
        tasks = [validate(session, i, userAgent) for i in urls]
        allowed_links = [link for link in await asyncio.gather(*tasks) if link]
        scraped = await asyncio.gather(
            *[(Scraping(session, link, userAgent)) for link in allowed_links]
        )
    return scraped
