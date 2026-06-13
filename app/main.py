from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.customer_routes import router as customer_router
from app.api.v1.order_routes import router as order_router
from app.api.v1.product_routes import router as product_router
from app.api.v1.payment_routes import router as payment_router
from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="FastAPI E-commerce API",
    version="1.0.0",
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)


@app.get("/")
def health_check():
    return {
        "message": "FastAPI is running",
    }


app.include_router(product_router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(payment_router)