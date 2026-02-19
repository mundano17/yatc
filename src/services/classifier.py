import re

import spacy

from src.models.scraper import Scrape

spacy_init = spacy.load("en_core_web_sm")


async def pre_processing(scraped_res: list[Scrape]) -> list[str]:
    res: list[str] = []
    for doc in scraped_res:
        processed_doc = re.sub(r"[^a-zA-z0-9\s\-]", "", doc.text)
        spacy_processed_doc = spacy_init(processed_doc)
        arr = [
            token.lemma_
            for token in spacy_processed_doc
            if not token.is_space and not token.is_punct and not token.is_stop
        ]
        print(arr)
        res.append(" ".join(arr))
    print(res)
    return res

