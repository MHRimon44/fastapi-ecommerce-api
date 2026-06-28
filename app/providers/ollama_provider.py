import json
import urllib.error
import urllib.request
from typing import List, Dict

from fastapi import HTTPException, status

from app.core.config import settings


class OllamaProvider:
    def __init__(self) -> None:
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.model_name = settings.OLLAMA_MODEL_NAME

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        payload = {
            "model": self.model_name,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        }

        request = urllib.request.Request(
            url=f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                response_body = response.read().decode("utf-8")
                data = json.loads(response_body)

                message = data.get("message") or {}
                content = message.get("content")

                if not content:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail="Ollama returned empty response",
                    )

                return content.strip()

        except urllib.error.URLError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Ollama is not available. Make sure Ollama is running. Error: {exc}",
            )


ollama_provider = OllamaProvider()
