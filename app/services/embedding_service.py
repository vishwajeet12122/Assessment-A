import os
import httpx

USF_BASE_URL = os.getenv("USF_BASE_URL")
USF_API_KEY = os.getenv("USF_API_KEY")
USF_EMBED_MODEL = os.getenv("USF_EMBED_MODEL")


async def get_embedding(text: str):
    url = f"{USF_BASE_URL}/embed/embeddings"

    headers = {
        "x-api-key": USF_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "model": USF_EMBED_MODEL,
        "input": text,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    return data["result"]["data"][0]["embedding"]