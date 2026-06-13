from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.product_routes import router as product_router
from app.db.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="FastAPI E-commerce API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def health_check():
    return {
        "message": "FastAPI is running",
    }


app.include_router(product_router)