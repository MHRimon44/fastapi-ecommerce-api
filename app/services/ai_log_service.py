import json
from typing import Any, Dict, List, Optional

from sqlmodel import Session

from app.models.ai_request_log_model import AIRequestLog
from app.repositories.ai_request_log_repository import ai_request_log_repository


class AILogService:
    def save_log(
        self,
        session: Session,
        module_name: str,
        endpoint: str,
        request_payload: Dict[str, Any],
        response_payload: Dict[str, Any],
        status_code: int,
        user_identifier: Optional[str] = None,
    ) -> AIRequestLog:
        log = AIRequestLog(
            module_name=module_name,
            endpoint=endpoint,
            status_code=status_code,
            user_identifier=user_identifier,
            request_body=self._to_json_string(request_payload),
            response_body=self._to_json_string(response_payload),
        )

        return ai_request_log_repository.create(
            session=session,
            log=log,
        )

    def get_recent_logs(
        self,
        session: Session,
        limit: int = 20,
    ) -> List[AIRequestLog]:
        return ai_request_log_repository.get_recent(
            session=session,
            limit=limit,
        )

    def _to_json_string(
        self,
        payload: Dict[str, Any],
    ) -> str:
        return json.dumps(
            payload,
            ensure_ascii=False,
            default=str,
        )


ai_log_service = AILogService()
