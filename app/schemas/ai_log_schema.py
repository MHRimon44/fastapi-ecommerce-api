from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AIRequestLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    log_id: int
    module_name: str
    endpoint: str
    status_code: int
    user_identifier: Optional[str]
    request_body: str
    response_body: str
    created_at: datetime


class AIRequestLogListResponse(BaseModel):
    message: str
    data: List[AIRequestLogRead]
