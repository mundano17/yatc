# STEP1: Preprocess
# STEP2: Lemmatize
# STEP3: TFIDF
# STEP4: GLOVEVECTORS
# STEP5: COSINE SIMILARITY
# STEP6: RETURN {LABEL: list[str] , .. ... ... }
# DONE

import re

from nltk.stem.wordnet import WordNetLemmatizer as wln
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from src.models.scraper import Scrape

count = CountVectorizer()


# removes everything that is not alphabets, digits and hypen
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


lemmatizer = wln()


# converts text -> vectors
async def feature_extractor(text: list[str]):
    lemmatized_text: list[str] = [
        " ".join([lemmatizer.lemmatize(token.lower()) for token in word_tokenize(doc)])
        for doc in text
    ]
    bag = count.fit_transform(lemmatized_text)
    tfidf = TfidfTransformer(norm="l2", use_idf=True)
    return tfidf.fit_transform(bag)
