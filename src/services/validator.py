from urllib.parse import urlparse

import aiohttp
from protego import Protego


async def validate(session: aiohttp.ClientSession, link: str, userAgent: str = "*"):
    robotUrl = f"{urlparse(link).scheme}://{urlparse(link).netloc}/robots.txt"
    try:
        async with session.get(robotUrl) as res:
            if res.status == 404:
                return link
            elif res.status == 200:
                robots = Protego.parse(await res.text())
                if robots.can_fetch(userAgent, link):
                    return link
            return False
    except aiohttp.ClientError as e:
        print("Validation error:", e)
        return False
