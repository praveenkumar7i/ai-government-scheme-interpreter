from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    status: str


class AskRequest(BaseModel):
    document_id: str
    question: str
    preferred_language: str = "en"
    target_languages: list[str] = ["hi", "kn", "ta", "te"]


class AskResponse(BaseModel):
    status: str
    answer: str
    eligibility: str
    citations: list[dict]
    confidence: float
    translations: dict[str, str]
    eligibility_reasoning: dict
