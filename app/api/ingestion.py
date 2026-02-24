from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import FinancialData
from app.core.auth import get_current_user
from app.core.rate_limiter import limiter
from app.services.embedding_service import get_embedding
from app.services.vector_service import upsert_vector
from app.api.websocket import broadcast

router = APIRouter(prefix="/data", tags=["financial-data"])


@router.post("/ingest")
@limiter.limit("10/minute")
async def ingest_data(
    request: Request,
    symbol: str,
    price: float,
    volume: int,
    news: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        # 🔹 1. Save structured data first
        new_record = FinancialData(
            symbol=symbol,
            price=price,
            volume=volume,
            news=news,
        )

        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)

        # 🔹 2. Generate embedding (external call)
        embedding = await get_embedding(news)

        # 🔹 3. Store in vector DB
        upsert_vector(
            record_id=new_record.id,
            vector=embedding,
            payload={
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "news": news,
            },
        )

        # 🔹 4. Broadcast to WebSocket clients
        await broadcast({
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "news": news
        })

        return {
            "message": "Data ingested successfully",
            "id": new_record.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )