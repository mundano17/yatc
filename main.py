import asyncio

import aiohttp

from src.services.classifier import pre_processing
from src.services.scraper import Scraping
from src.services.validator import validate

urls = [
    "https://economictimes.indiatimes.com/news/economy/foreign-trade/the-two-revisions-in-india-us-trade-deal-factsheet-by-white-house-tariff-on-pulses-removed-donald-trump-narendra-modi-intends-to-purchase-500-billion-goods/articleshow/128184777.cms",
    "https://economictimes.indiatimes.com/news/economy/foreign-trade/india-us-trade-deal-america-has-stopped-short-of-indian-red-lines/articleshow/128024443.cms",
]


async def yatc(urls: list[str], userAgent: str = "*"):
    async with aiohttp.ClientSession() as session:
        tasks = [validate(session, i, userAgent) for i in urls]
        allowed_links = [link for link in await asyncio.gather(*tasks) if link]
        scraped = await asyncio.gather(
            *[(Scraping(session, link, userAgent)) for link in allowed_links]
        )
        if len(scraped) > 0:
            preprocessed_array = await pre_processing(scraped)


asyncio.run(yatc(urls))
