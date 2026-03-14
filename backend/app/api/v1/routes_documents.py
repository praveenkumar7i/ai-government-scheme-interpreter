from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import SchemeDocument
from app.schemas.document import DocumentUploadResponse
from app.services.ingestion_service import process_pdf, save_uploaded_file

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    scheme_name: str = Form(...),
    scheme_year: int | None = Form(None),
    state: str | None = Form(None),
    db: Session = Depends(get_db),
):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = save_uploaded_file(await file.read(), filename)

    doc = SchemeDocument(
        scheme_name=scheme_name,
        scheme_year=scheme_year,
        state=state,
        file_path=file_path,
        processing_status="processing",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    process_pdf(doc.id, db)
    return DocumentUploadResponse(document_id=str(doc.id), status="ready")
