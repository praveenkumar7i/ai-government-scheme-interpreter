from __future__ import annotations

import uuid
from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import DocumentChunk, SchemeDocument
from app.services.vector_store_service import upsert_chunks


def _chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return [c.strip() for c in chunks if c.strip()]


def process_pdf(document_id: uuid.UUID, db: Session) -> int:
    document = db.query(SchemeDocument).filter(SchemeDocument.id == document_id).first()
    if not document:
        return 0

    reader = PdfReader(document.file_path)
    all_chunks: list[dict] = []
    chunk_count = 0

    for page_idx, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        for i, chunk in enumerate(_chunk_text(raw)):
            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk_count,
                page_number=page_idx,
                section_title=f"Page {page_idx}",
                content=chunk,
            )
            db.add(db_chunk)
            all_chunks.append(
                {
                    "id": str(db_chunk.id),
                    "content": chunk,
                    "metadata": {
                        "document_id": str(document.id),
                        "page_number": page_idx,
                        "section_title": f"Page {page_idx}",
                    },
                }
            )
            chunk_count += 1

    document.processing_status = "ready"
    db.commit()

    if all_chunks:
        upsert_chunks(all_chunks)
    return chunk_count


def save_uploaded_file(file_bytes: bytes, filename: str) -> str:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / filename
    path.write_bytes(file_bytes)
    return str(path)
