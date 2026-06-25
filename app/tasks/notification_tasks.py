import os
from datetime import datetime


def enqueue_notification_task(
    channel: str,
    message: str,
) -> None:
    os.makedirs("logs", exist_ok=True)

    log_message = (
        f"[{datetime.utcnow()}] NOTIFICATION QUEUED\n"
        f"Channel: {channel}\n"
        f"Message: {message}\n"
        f"{'-' * 50}\n"
    )

    with open("logs/notification_queue.log", "a") as file:
        file.write(log_message)