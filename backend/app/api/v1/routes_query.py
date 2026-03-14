from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.chat import ChatMessage, ChatSession
from app.models.user import User
from app.schemas.document import AskRequest, AskResponse
from app.services.rag_service import ask_question
from app.services.sarvam_service import SarvamService

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = ask_question(request.document_id, request.question)

    sarvam = SarvamService()
    translations = {lang: sarvam.translate(result["answer"], lang) for lang in request.target_languages}

    session = ChatSession(user_id=current_user.id, document_id=uuid.UUID(request.document_id))
    db.add(session)
    db.flush()

    db.add(ChatMessage(session_id=session.id, role="user", message_text=request.question, language=request.preferred_language))
    db.add(ChatMessage(session_id=session.id, role="assistant", message_text=result["answer"], language=request.preferred_language))
    db.commit()

    return AskResponse(
        status="success",
        answer=result["answer"],
        eligibility=result["eligibility"],
        citations=result["citations"],
        confidence=result["confidence"],
        translations=translations,
        eligibility_reasoning=result["eligibility_reasoning"],
    )
