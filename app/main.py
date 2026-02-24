from fastapi import FastAPI
from dotenv import load_dotenv
from app.db.database import engine, Base

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from app.core.rate_limiter import limiter
from app.api import auth, ingestion, query, websocket
from app.services.vector_service import init_collection

load_dotenv()


app = FastAPI(
    title="Real-time Financial Analytics - Test A",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(ingestion.router)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(query.router)
app.include_router(websocket.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    init_collection()    

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )

@app.get("/")
async def health():
    return {"status": "running"}