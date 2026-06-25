from pathlib import Path

from app.tasks.email_tasks import send_email_task
from app.tasks.notification_tasks import enqueue_notification_task
from app.tasks.report_tasks import generate_sales_report_task
from app.tasks.ai_tasks import parse_text_with_ai_task


def test_send_email_task_creates_log():
    send_email_task(
        to_email="rahim@example.com",
        subject="Test Email",
        body="This is a test email.",
    )

    log_file = Path("logs/emails.log")

    assert log_file.exists()
    assert "rahim@example.com" in log_file.read_text()


def test_enqueue_notification_task_creates_log():
    enqueue_notification_task(
        channel="admin",
        message="New order placed",
    )

    log_file = Path("logs/notification_queue.log")

    assert log_file.exists()
    assert "New order placed" in log_file.read_text()


def test_generate_sales_report_task_creates_report():
    generate_sales_report_task(
        report_name="test_sales",
    )

    reports = list(Path("generated_reports").glob("test_sales_*.csv"))

    assert len(reports) > 0


def test_parse_text_with_ai_task_creates_log():
    parse_text_with_ai_task(
        document_type="purchase_order",
        text="PO Number 1001. Buyer ABC Fashion. Quantity 500 pieces.",
    )

    log_file = Path("logs/ai_parsing.log")

    assert log_file.exists()
    assert "purchase_order" in log_file.read_text()