import os
from datetime import datetime


def parse_text_with_ai_task(
    document_type: str,
    text: str,
) -> None:
    os.makedirs("logs", exist_ok=True)

    # This is a fake AI parsing result for learning.
    # Later you can replace this with OpenAI/local LLM call.
    short_text = text[:200].replace("\n", " ")

    message = (
        f"[{datetime.utcnow()}] AI PARSING COMPLETED\n"
        f"Document type: {document_type}\n"
        f"Extracted summary: {short_text}\n"
        f"{'-' * 50}\n"
    )

    with open("logs/ai_parsing.log", "a") as file:
        file.write(message)