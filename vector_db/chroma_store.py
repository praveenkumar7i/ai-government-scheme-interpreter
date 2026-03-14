from __future__ import annotations

import os
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

COLLECTION_NAME = "scheme_chunks"
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./vector_db/chroma_data")
EMBEDDING_MODEL = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


def get_collection(
    persist_dir: str = PERSIST_DIR,
    collection_name: str = COLLECTION_NAME,
    embedding_model: str = EMBEDDING_MODEL,
):
    client = chromadb.PersistentClient(path=persist_dir)
    embedding_fn = SentenceTransformerEmbeddingFunction(model_name=embedding_model)
    return client.get_or_create_collection(name=collection_name, embedding_function=embedding_fn)


def upsert_chunks(chunks: list[dict[str, Any]]) -> None:
    collection = get_collection()
    collection.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["content"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )


def vector_search(query: str, document_id: str, k: int = 8) -> list[dict[str, Any]]:
    collection = get_collection()
    result = collection.query(query_texts=[query], n_results=k, where={"document_id": document_id})

    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    dists = result.get("distances", [[]])[0]

    return [
        {
            "content": doc,
            "metadata": meta,
            "score": max(0.0, 1 - float(dist)),
        }
        for doc, meta, dist in zip(docs, metas, dists)
    ]
