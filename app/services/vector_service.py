import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

QDRANT_URL = os.getenv("QDRANT_URL")

client = QdrantClient(url=QDRANT_URL)

COLLECTION_NAME = "financial_news"


def init_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,  # adjust if embed size differs
                distance=Distance.COSINE,
            ),
        )


def upsert_vector(record_id: int, vector: list, payload: dict):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=record_id,
                vector=vector,
                payload=payload,
            )
        ],
    )


def search_vector(query_vector: list, limit: int = 5):
    return client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
    )