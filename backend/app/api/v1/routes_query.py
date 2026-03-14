from fastapi import APIRouter

from app.schemas.document import AskRequest, AskResponse
from app.services.sarvam_service import SarvamService
from app.services.rag_service import ask_question

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    result = ask_question(request.document_id, request.question)

    sarvam = SarvamService()
    translations = {
        lang: sarvam.translate(result["answer"], lang)
        for lang in request.target_languages
    }

    return AskResponse(
        status="success",
        answer=result["answer"],
        eligibility=result["eligibility"],
        citations=result["citations"],
        confidence=result["confidence"],
        translations=translations,
        eligibility_reasoning=result["eligibility_reasoning"],
    )
