import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.models.scraper import Scrape


class Classifier:
    def __init__(self, documents: list[Scrape], labels: list[str]):
        self.documents = documents
        self.labels = labels
        self.device = "cpu"
        if torch.cuda.is_available():
            self.device = "cuda"
        if torch.backends.mps.is_available():
            self.device = "mps"
        self.model = SentenceTransformer("all-mpnet-base-v2", device=self.device)

        self.label_embeddings = self.model.encode(
            [f"the text is about {label}." for label in labels],
            convert_to_numpy=True,
        )

    def chunk_text(
        self, text: str, chunk_size: int = 150, overlap: int = 15
    ) -> list[str]:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        words = text.strip().split()
        return [
            " ".join(words[i : min(i + chunk_size, len(words))])
            for i in range(0, len(words), chunk_size - overlap)
        ]

    def __call__(self) -> list[str]:
        all_doc_chunks = [self.chunk_text(doc.text) for doc in self.documents]

        flat_chunks = [chunk for doc in all_doc_chunks for chunk in doc]

        if not flat_chunks:
            return []

        chunk_embeddings = self.model.encode(
            flat_chunks,
            convert_to_numpy=True,
            batch_size=32,
            show_progress_bar=True,
        )

        similarities = cosine_similarity(chunk_embeddings, self.label_embeddings)

        results = []
        cursor = 0

        for doc_chunks in all_doc_chunks:
            doc_len = len(doc_chunks)
            doc_sim = similarities[cursor : cursor + doc_len]
            cursor += doc_len
            avg_sim = doc_sim.mean(axis=0)
            best_label = self.labels[np.argmax(avg_sim)]
            results.append(best_label)

        return results
