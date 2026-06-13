from fastapi import FastAPI

from app.api.v1.product_routes import router as product_router

app = FastAPI(
    title="FastAPI E-commerce API",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {
        "message": "FastAPI is running",
    }


app.include_router(product_router)