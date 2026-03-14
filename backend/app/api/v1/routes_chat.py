from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.chat import ChatMessage, ChatSession
from app.models.user import User
from app.schemas.chat import ChatHistoryItem

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/history", response_model=list[ChatHistoryItem])
def get_chat_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(ChatSession.id, ChatMessage.role, ChatMessage.message_text, ChatMessage.created_at)
        .join(ChatMessage, ChatMessage.session_id == ChatSession.id)
        .filter(ChatSession.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(100)
        .all()
    )

    return [
        ChatHistoryItem(session_id=str(r.id), role=r.role, message_text=r.message_text, created_at=r.created_at)
        for r in rows
    ]
