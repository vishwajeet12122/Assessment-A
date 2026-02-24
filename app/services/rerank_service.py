import os
import httpx

USF_BASE_URL = os.getenv("USF_BASE_URL")
USF_API_KEY = os.getenv("USF_API_KEY")
USF_RERANK_MODEL = os.getenv("USF_RERANK_MODEL")


async def rerank(query: str, texts: list[str]):
    url = f"{USF_BASE_URL}/embed/reranker"

    headers = {
        "x-api-key": USF_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "model": USF_RERANK_MODEL,
        "query": query,
        "texts": texts,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    return data["result"]["data"]