# Real-Time Financial Analytics with Semantic Filtering (Test A)

## Overview

This project implements a FastAPI-based real-time financial analytics
system with:

-   Streaming data ingestion
-   WebSocket support
-   Retrieval-Augmented Generation (RAG)
-   Hybrid structured + semantic search
-   Reranking
-   Authentication
-   Rate limiting
-   Redis caching

The system processes financial market data and news in real-time and
allows semantically enriched querying with improved relevance using
reranking.

------------------------------------------------------------------------

# 1. Complete Code Repository with Installation Instructions

## Project Structure

    assessment-A/
    │
    ├── app/
    │   ├── main.py
    │   ├── core/
    │   ├── db/
    │   ├── services/
    │   └── api/
    │
    ├── docker-compose.yml
    ├── requirements.txt
    └── .env

------------------------------------------------------------------------

## Installation Instructions

### Step 1: Clone Repository

    git clone <your-repo-url>
    cd assessment-A

### Step 2: Create Virtual Environment

Windows:

    python -m venv venv
    venv\Scripts\activate

Mac/Linux:

    python3 -m venv venv
    source venv/bin/activate

### Step 3: Install Dependencies

    pip install -r requirements.txt

### Step 4: Start Infrastructure (Qdrant + Redis)

    docker compose up -d

### Step 5: Configure Environment Variables

Create `.env` file:

    USF_BASE_URL=https://api.us.inc/usf/v1/hiring
    USF_API_KEY=YOUR_KEY

    USF_CHAT_MODEL=usf1-mini
    USF_EMBED_MODEL=usf1-embed
    USF_RERANK_MODEL=usf1-rerank

    QDRANT_URL=http://localhost:6333
    REDIS_URL=redis://localhost:6379/0

    JWT_SECRET=supersecret
    JWT_ALG=HS256

### Step 6: Run Application

    uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 2. Documentation Explaining Implementation Details

## Architecture Overview

Client → FastAPI → SQLite (structured data)\
→ Qdrant (vector storage)\
→ Redis (caching)\
→ USF API (embeddings + rerank)

------------------------------------------------------------------------

## Data Ingestion Flow

1.  User sends financial data (symbol, price, volume, news).
2.  JWT authentication validated.
3.  Data stored in SQLite.
4.  News text embedded using USF embedding API.
5.  Vector stored in Qdrant.
6.  Data broadcast to WebSocket clients.

------------------------------------------------------------------------

## Query Flow (Hybrid RAG)

1.  Query received.
2.  Redis cache checked.
3.  Structured filter applied (optional symbol).
4.  Query embedded.
5.  Vector similarity search (Top-K).
6.  Reranking via USF reranker.
7.  Results cached and returned.

------------------------------------------------------------------------

## WebSocket Support

-   `/ws` endpoint
-   Broadcasts newly ingested data to connected clients
-   Enables real-time streaming

------------------------------------------------------------------------

# 3. Design Decisions and Trade-offs

## Why SQLite?

Used for simplicity in assessment context. Easily replaceable with
PostgreSQL in production.

## Why Qdrant?

High-performance vector database optimized for semantic search and
hybrid filtering.

## Why Hybrid Search?

Combines structured filtering (precision) with semantic similarity
(recall).

## Why Reranking?

Vector similarity alone may produce approximate matches. Reranking
improves relevance quality.

## Trade-offs

-   Embeddings generated synchronously (could be background task in
    production).
-   SQLite limits horizontal scalability.
-   Redis caching based on query key only (could improve with hashed
    keys + metadata).

------------------------------------------------------------------------

# 4. Performance Considerations

## Asynchronous Architecture

-   Async SQLAlchemy
-   Async HTTP calls
-   Non-blocking request lifecycle

## Caching Strategy

-   Redis cache
-   TTL = 5 minutes
-   Reduces API usage and latency

## Vector Search Optimization

-   Top-K retrieval
-   Cosine similarity
-   Rerank only limited candidates

## Rate Limiting

-   10 requests/minute
-   Protects API resources
-   Prevents misuse

------------------------------------------------------------------------

# 5. Extensions and Improvements (Given More Time)

-   Move embedding generation to background task queue (Celery/Kafka)
-   Add database indexing and optimized filtering
-   Implement Qdrant filtering inside vector search
-   Add monitoring (Prometheus + Grafana)
-   Add circuit breaker for external API
-   Add load testing benchmarks
-   Implement retry logic for failed embeddings
-   Add multi-tenant support

------------------------------------------------------------------------

# Completion Status

✔ FastAPI implementation\
✔ Authentication\
✔ Rate limiting\
✔ WebSocket support\
✔ Embedding integration\
✔ Vector database integration\
✔ Reranking\
✔ Hybrid search\
✔ Redis caching
