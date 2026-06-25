import os
from datetime import datetime


def send_email_task(
    to_email: str,
    subject: str,
    body: str,
) -> None:
    os.makedirs("logs", exist_ok=True)

    log_message = (
        f"[{datetime.utcnow()}] EMAIL SENT\n"
        f"To: {to_email}\n"
        f"Subject: {subject}\n"
        f"Body: {body}\n"
        f"{'-' * 50}\n"
    )

    with open("logs/emails.log", "a") as file:
        file.write(log_message)