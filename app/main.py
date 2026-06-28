from app.api.v1.admin_report_routes import router as admin_report_router
from app.api.v1.admin_user_routes import router as admin_user_router
from app.api.v1.erp_policy_routes import router as erp_policy_router
from app.api.v1.company_document_routes import router as company_document_router
from app.api.v1.business_ai_routes import router as business_ai_router
from app.api.v1.ai_commerce_routes import router as ai_commerce_router
from app.api.v1.ai_log_routes import router as ai_log_router
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
from app.api.v1.support_knowledge_routes import router as support_knowledge_router
from app.api.v1.voucher_routes import router as voucher_router
from app.api.v1.admin_product_routes import router as admin_product_router
from app.api.v1.admin_customer_routes import router as admin_customer_router
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
app.include_router(support_knowledge_router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(rag_router)
app.include_router(voucher_router)
app.include_router(auth_router)
app.include_router(background_router)
app.include_router(document_router)
app.include_router(ai_router)
app.include_router(erp_policy_router)
app.include_router(company_document_router)
app.include_router(business_ai_router)
app.include_router(ai_commerce_router)
app.include_router(ai_log_router)
app.include_router(admin_user_router)
app.include_router(admin_report_router)
app.include_router(admin_product_router)
app.include_router(admin_customer_router)
