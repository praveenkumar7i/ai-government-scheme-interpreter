from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    document_id: str
    status: str


class DocumentListItem(BaseModel):
    id: str
    scheme_name: str
    scheme_code: str | None
    scheme_year: int | None
    state: str | None
    source_language: str | None
    processing_status: str
    total_pages: int | None


class AskRequest(BaseModel):
    document_id: str = Field(min_length=36, max_length=36)
    question: str = Field(min_length=5, max_length=2000)
    preferred_language: str = Field(default="en", min_length=2, max_length=5)
    target_languages: list[str] = ["hi", "kn", "ta", "te"]


class AskResponse(BaseModel):
    status: str
    answer: str
    eligibility: str
    citations: list[dict]
    confidence: float
    translations: dict[str, str]
    eligibility_reasoning: dict
