from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
)

from app.api.v1.product_routes import router as product_router
from app.api.v1.customer_routes import router as customer_router
from app.api.v1.order_routes import router as order_router
from app.api.v1.payment_routes import router as payment_router
from app.api.v1.voucher_routes import router as voucher_router
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.background_routes import router as background_router


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(voucher_router)
app.include_router(auth_router)
app.include_router(background_router)