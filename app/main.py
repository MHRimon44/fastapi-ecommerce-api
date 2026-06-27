import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.ai_routes import router as ai_router
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.background_routes import router as background_router
from app.api.v1.document_routes import router as document_router
from app.api.v1.customer_routes import router as customer_router
from app.api.v1.order_routes import router as order_router
from app.api.v1.payment_routes import router as payment_router
from app.api.v1.rag_routes import router as rag_router
from app.api.v1.product_routes import router as product_router
from app.api.v1.product_knowledge_routes import router as product_knowledge_router
from app.api.v1.voucher_routes import router as voucher_router
from app.core.config import settings
from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
)
from app.core.logger import get_logger, setup_logging


setup_logging()
logger = get_logger(__name__)


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


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)

        process_time = round(
            (time.time() - start_time) * 1000,
            2,
        )

        logger.info(
            "%s %s completed with status %s in %sms",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response

    except Exception:
        process_time = round(
            (time.time() - start_time) * 1000,
            2,
        )

        logger.exception(
            "%s %s failed after %sms",
            request.method,
            request.url.path,
            process_time,
        )

        raise


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
app.include_router(product_knowledge_router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(rag_router)
app.include_router(voucher_router)
app.include_router(auth_router)
app.include_router(background_router)
app.include_router(document_router)
app.include_router(ai_router)
