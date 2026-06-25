from datetime import datetime


def send_order_confirmation_notification(order_no: str) -> None:
    """
    This simulates sending an order confirmation email/notification.

    In production, this function could call:
    - SMTP server
    - SendGrid
    - Mailgun
    - AWS SES
    - SMS gateway
    - Push notification service
    """

    message = (
        f"[{datetime.utcnow()}] "
        f"Order confirmation generated for order_no={order_no}\n"
    )

    with open("logs/order_notifications.log", "a") as file:
        file.write(message)