import re

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from src.models.scraper import Scrape

count = CountVectorizer()


async def pre_processing(scraped_res: list[Scrape]) -> list[str]:
    res: list[str] = []
    for i in range(len(scraped_res)):
        arr = scraped_res[i].text.split("\n")
        for j in range(len(arr)):
            if arr[j] != "":
                arr[j] = re.sub(r"[^a-zA-Z0-9\s-]", "", arr[j]).strip()
            else:
                continue

        res.append(" ".join(arr))
    return res


async def feature_extractor(text: list[str]):
    bag = count.fit_transform(text)
    tfidf = TfidfTransformer(norm="l2", use_idf=True)
    return tfidf.fit_transform(bag)
