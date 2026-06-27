from typing import List

from sqlmodel import Session, select

from app.models.ai_request_log_model import AIRequestLog


class AIRequestLogRepository:
    def create(
        self,
        session: Session,
        log: AIRequestLog,
    ) -> AIRequestLog:
        session.add(log)
        session.commit()
        session.refresh(log)

        return log

    def get_recent(
        self,
        session: Session,
        limit: int = 20,
    ) -> List[AIRequestLog]:
        statement = (
            select(AIRequestLog)
            .order_by(AIRequestLog.created_at.desc())
            .limit(limit)
        )

        return list(session.exec(statement).all())


ai_request_log_repository = AIRequestLogRepository()
