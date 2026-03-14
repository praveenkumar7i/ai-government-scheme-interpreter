from __future__ import annotations

import re
import uuid
from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import DocumentChunk, SchemeDocument
from app.services.vector_store_service import upsert_chunks

HEADING_PATTERNS = [
    re.compile(r"^\d+(\.\d+)*\s+[A-Z][A-Za-z\s\-/,&()]+$"),
    re.compile(r"^[A-Z][A-Z\s\-/,&()]{4,}$"),
    re.compile(r"^(Eligibility|Benefits|Documents Required|How to Apply|Scope)\s*:?$", re.IGNORECASE),
]


def _is_heading(line: str) -> bool:
    candidate = line.strip()
    if not candidate or len(candidate.split()) > 12:
        return False
    return any(pattern.match(candidate) for pattern in HEADING_PATTERNS)


def _split_by_headings(page_text: str) -> list[tuple[str, str]]:
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    sections: list[tuple[str, str]] = []
    current_heading = "General"
    buffer: list[str] = []

    for line in lines:
        if _is_heading(line):
            if buffer:
                sections.append((current_heading, "\n".join(buffer)))
                buffer = []
            current_heading = line
        else:
            buffer.append(line)

    if buffer:
        sections.append((current_heading, "\n".join(buffer)))
    return sections


def _window_chunk(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    words = text.split(" ")
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words).strip()
        if chunk:
            chunks.append(chunk)
        if end == len(words):
            break
        start = max(0, end - overlap)
    return chunks


def process_pdf(document_id: uuid.UUID, db: Session) -> int:
    document = db.query(SchemeDocument).filter(SchemeDocument.id == document_id).first()
    if not document:
        return 0

    reader = PdfReader(document.file_path)
    all_chunks: list[dict] = []
    chunk_count = 0

    for page_idx, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        for section_title, section_text in _split_by_headings(raw):
            for chunk in _window_chunk(section_text):
                db_chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=chunk_count,
                    page_number=page_idx,
                    section_title=section_title,
                    content=chunk,
                )
                db.add(db_chunk)
                db.flush()
                all_chunks.append(
                    {
                        "id": str(db_chunk.id),
                        "content": chunk,
                        "metadata": {
                            "document_id": str(document.id),
                            "page_number": page_idx,
                            "section_title": section_title,
                            "chunk_index": chunk_count,
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
