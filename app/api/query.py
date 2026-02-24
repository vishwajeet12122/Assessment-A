from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.models import FinancialData
from app.core.auth import get_current_user
from app.core.rate_limiter import limiter
from app.services.embedding_service import get_embedding
from app.services.vector_service import search_vector
from app.services.rerank_service import rerank
from app.services.cache_service import get_cache, set_cache


router = APIRouter(prefix="/query", tags=["search"])


@router.post("/")
@limiter.limit("10/minute")
async def search_data(
    request: Request,
    query: str,
    symbol: str | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    cache_key = f"{query}:{symbol}"
    cached = get_cache(cache_key)
    if cached:
        return {"results": cached}

    stmt = select(FinancialData)
    if symbol:
        stmt = stmt.where(FinancialData.symbol == symbol)

    result = await db.execute(stmt)
    structured_results = result.scalars().all()

    if not structured_results:
        return {"results": []}

    query_vector = await get_embedding(query)

    vector_results = search_vector(query_vector, limit=5)

    if not vector_results:
        return {"results": []}

    texts = [res.payload["news"] for res in vector_results]

    reranked = await rerank(query, texts)

    final_results = []
    for item in reranked:
        index = item["index"]
        score = item["score"]
        original = vector_results[index]

        if symbol and original.payload["symbol"] != symbol:
            continue

        final_results.append({
            "id": original.id,
            "symbol": original.payload["symbol"],
            "news": original.payload["news"],
            "score": score,
        })

    set_cache(cache_key, final_results)

    return {"results": final_results}