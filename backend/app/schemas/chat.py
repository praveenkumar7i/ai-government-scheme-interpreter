from datetime import datetime

from pydantic import BaseModel


class ChatHistoryItem(BaseModel):
    session_id: str
    role: str
    message_text: str
    created_at: datetime
