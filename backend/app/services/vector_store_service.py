from __future__ import annotations

from typing import Any

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from app.core.config import settings

COLLECTION_NAME = "scheme_chunks"


def _collection():
    client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    embedding_fn = SentenceTransformerEmbeddingFunction(model_name=settings.embeddings_model)
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)


def upsert_chunks(chunks: list[dict[str, Any]]) -> None:
    collection = _collection()
    collection.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["content"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )


def search_chunks(query: str, document_id: str, k: int = 4) -> list[dict[str, Any]]:
    collection = _collection()
    result = collection.query(query_texts=[query], n_results=k, where={"document_id": document_id})
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    dists = result.get("distances", [[]])[0]
    return [{"content": d, "metadata": m, "score": 1 - float(s)} for d, m, s in zip(docs, metas, dists)]
