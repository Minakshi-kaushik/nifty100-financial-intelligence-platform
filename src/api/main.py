"""
main.py

FastAPI Application
Sprint 6
"""

import time

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    health,
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
)

app = FastAPI(
    title="NIFTY100 Financial Analytics API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logger(request, call_next):

    start = time.time()

    response = await call_next(request)

    elapsed = round(time.time() - start, 3)

    print(f"{request.method} {request.url.path} {elapsed}s")

    return response


# =====================================================
# ROUTERS
# =====================================================

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    companies.router,
    prefix="/api/v1",
    tags=["Companies"],
)

app.include_router(
    screener.router,
    prefix="/api/v1",
    tags=["Screener"],
)

app.include_router(
    sectors.router,
    prefix="/api/v1",
    tags=["Sectors"],
)

app.include_router(
    peers.router,
    prefix="/api/v1",
    tags=["Peers"],
)

app.include_router(
    valuation.router,
    prefix="/api/v1",
    tags=["Valuation"],
)

app.include_router(
    portfolio.router,
    prefix="/api/v1",
    tags=["Portfolio"],
)

app.include_router(
    documents.router,
    prefix="/api/v1",
    tags=["Documents"],
)


@app.get("/")
def root():

    return {
        "project": "NIFTY100 Financial Analytics",
        "version": "1.0.0",
        "docs": "/docs",
    }
