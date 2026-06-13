from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def _format_validation_message(error: dict) -> str:
    loc = error.get("loc", [])
    msg = error.get("msg", "Invalid request")

    field_name = None

    for item in reversed(loc):
        if isinstance(item, str) and item != "body":
            field_name = item
            break

    if field_name == "phone":
        return "Phone number must be a valid Bangladeshi mobile number. Example: 01700000000"

    if field_name == "email":
        return "Email address must be in a valid format. Example: customer@example.com"

    if field_name == "product_name":
        return f"Product name validation failed: {msg}"

    if field_name == "password":
        return "Password must be between 6 and 72 characters"

    if field_name == "price":
        return f"Price validation failed: {msg}"

    if field_name == "stock_qty":
        return f"Stock quantity validation failed: {msg}"

    if field_name:
        return f"{field_name} validation failed: {msg}"

    return msg


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    message = exc.detail if isinstance(exc.detail, str) else "Request failed"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": message,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = exc.errors()

    if not errors:
        message = "Invalid request data"
    else:
        message = _format_validation_message(errors[0])

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": message,
        },
    )