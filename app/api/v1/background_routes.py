import shutil
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile, status

from app.schemas.background_schema import (
    AIParseRequest,
    EmailTaskRequest,
    NotificationTaskRequest,
    ReportTaskRequest,
)
from app.schemas.common_schema import MessageResponse
from app.tasks.ai_tasks import parse_text_with_ai_task
from app.tasks.email_tasks import send_email_task
from app.tasks.notification_tasks import enqueue_notification_task
from app.tasks.pdf_tasks import process_pdf_task
from app.tasks.report_tasks import generate_sales_report_task


router = APIRouter(
    prefix="/background",
    tags=["Background Tasks"],
)


@router.post(
    "/email/send",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def send_email(
    request: EmailTaskRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        send_email_task,
        request.to_email,
        request.subject,
        request.body,
    )

    return MessageResponse(
        message="Email sending started successfully",
    )


@router.post(
    "/notifications/enqueue",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def enqueue_notification(
    request: NotificationTaskRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        enqueue_notification_task,
        request.channel,
        request.message,
    )

    return MessageResponse(
        message="Notification queued successfully",
    )


@router.post(
    "/reports/sales-summary",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_sales_report(
    request: ReportTaskRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        generate_sales_report_task,
        request.report_name,
    )

    return MessageResponse(
        message="Report generation started successfully",
    )


@router.post(
    "/pdf/process",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def process_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    upload_dir = Path("uploads/pdf")
    upload_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    safe_filename = Path(file.filename).name
    saved_file_path = upload_dir / f"{timestamp}_{safe_filename}"

    with saved_file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    background_tasks.add_task(
        process_pdf_task,
        str(saved_file_path),
    )

    return MessageResponse(
        message="PDF processing started successfully",
    )


@router.post(
    "/ai/parse-text",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def parse_text_with_ai(
    request: AIParseRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        parse_text_with_ai_task,
        request.document_type,
        request.text,
    )

    return MessageResponse(
        message="AI parsing started successfully",
    )