from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.document import SchemeDocument
from app.models.user import User
from app.schemas.document import DocumentListItem, DocumentUploadResponse
from app.services.ingestion_service import process_pdf, save_uploaded_file

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    scheme_name: str = Form(...),
    scheme_code: str | None = Form(None),
    scheme_year: int | None = Form(None),
    state: str | None = Form(None),
    source_language: str | None = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_bytes = await file.read()
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = save_uploaded_file(file_bytes, filename)

    doc = SchemeDocument(
        uploaded_by=current_user.id,
        scheme_name=scheme_name,
        scheme_code=scheme_code,
        scheme_year=scheme_year,
        state=state,
        source_language=source_language,
        file_path=file_path,
        file_hash=hashlib.sha256(file_bytes).hexdigest(),
        processing_status="processing",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    process_pdf(doc.id, db)

    return DocumentUploadResponse(document_id=str(doc.id), status="ready")


@router.get("", response_model=list[DocumentListItem])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    docs = (
        db.query(SchemeDocument)
        .filter(SchemeDocument.uploaded_by == current_user.id)
        .order_by(SchemeDocument.created_at.desc())
        .all()
    )
    return [
        DocumentListItem(
            id=str(d.id),
            scheme_name=d.scheme_name,
            scheme_code=d.scheme_code,
            scheme_year=d.scheme_year,
            state=d.state,
            source_language=d.source_language,
            processing_status=d.processing_status,
            total_pages=d.total_pages,
        )
        for d in docs
    ]
