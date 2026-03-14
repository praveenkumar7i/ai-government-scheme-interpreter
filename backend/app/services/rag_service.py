from __future__ import annotations

import math
import re
import uuid
from collections import Counter
from dataclasses import dataclass

from langchain.prompts import PromptTemplate

from app.db.session import SessionLocal
from app.models.document import DocumentChunk
from app.services.sarvam_service import SarvamService
from app.services.vector_store_service import search_chunks

PROMPT = PromptTemplate.from_template(
    """
You explain Indian government schemes in simple language.
Use ONLY the provided context and cite the page references as [pX].
If context is insufficient, say 'Insufficient Data'.

Question: {question}
Eligibility signals extracted: {signals}

Context:
{context}

Return JSON with keys:
- answer
- eligibility_verdict (Likely Eligible/Possibly Eligible/Not Eligible/Insufficient Data)
- rationale
"""
)

TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
INCOME_RE = re.compile(r"(?:income|annual income|yearly income)[^\d]{0,30}(\d+(?:\.\d+)?)\s*(lakh|lac|crore)?", re.IGNORECASE)
AGE_RE = re.compile(r"(?:age|aged|between)\D{0,15}(\d{1,2})\D{0,6}(?:to|-)?\D{0,6}(\d{1,2})?", re.IGNORECASE)


@dataclass
class EligibilitySignals:
    user_income_lakh: float | None
    user_age: int | None
    doc_income_limit_lakh: float | None
    doc_min_age: int | None
    doc_max_age: int | None


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def _bm25_score(query: str, doc: str, avgdl: float, doc_freqs: Counter[str], n_docs: int, k1: float = 1.5, b: float = 0.75) -> float:
    q_tokens = _tokenize(query)
    d_tokens = _tokenize(doc)
    dl = len(d_tokens) or 1
    freqs = Counter(d_tokens)
    score = 0.0

    for term in q_tokens:
        if term not in freqs:
            continue
        df = doc_freqs.get(term, 0)
        idf = math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
        tf = freqs[term]
        numer = tf * (k1 + 1)
        denom = tf + k1 * (1 - b + b * dl / (avgdl or 1))
        score += idf * (numer / denom)
    return score


def _hybrid_retrieve(document_id: str, question: str, top_k: int = 4) -> list[dict]:
    vector_hits = search_chunks(query=question, document_id=document_id, k=10)
    vector_map = {
        (str(hit["metadata"].get("page_number")), str(hit["metadata"].get("chunk_index"))): hit
        for hit in vector_hits
    }

    with SessionLocal() as db:
        db_chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == uuid.UUID(document_id)).all()

    if not db_chunks:
        return vector_hits[:top_k]

    docs_text = [chunk.content for chunk in db_chunks]
    n_docs = len(docs_text)
    avgdl = sum(len(_tokenize(t)) for t in docs_text) / max(n_docs, 1)
    doc_freqs: Counter[str] = Counter()
    for text in docs_text:
        for tok in set(_tokenize(text)):
            doc_freqs[tok] += 1

    bm25_ranked = []
    for chunk in db_chunks:
        score = _bm25_score(question, chunk.content, avgdl, doc_freqs, n_docs)
        if score > 0:
            bm25_ranked.append((score, chunk))

    bm25_ranked.sort(key=lambda x: x[0], reverse=True)

    merged: dict[tuple[str, str], dict] = {}

    for rank, hit in enumerate(vector_hits):
        key = (str(hit["metadata"].get("page_number")), str(hit["metadata"].get("chunk_index")))
        merged[key] = {
            "content": hit["content"],
            "metadata": hit["metadata"],
            "hybrid_score": (0.7 * float(hit.get("score", 0))) + (0.3 * (1 / (1 + rank))),
        }

    for rank, (bm25_score, chunk) in enumerate(bm25_ranked[:20]):
        key = (str(chunk.page_number), str(chunk.chunk_index))
        payload = merged.get(
            key,
            {
                "content": chunk.content,
                "metadata": {
                    "page_number": chunk.page_number,
                    "section_title": chunk.section_title,
                    "chunk_index": chunk.chunk_index,
                    "document_id": document_id,
                },
                "hybrid_score": 0.0,
            },
        )
        payload["hybrid_score"] += (0.5 * bm25_score) + (0.2 * (1 / (1 + rank)))
        merged[key] = payload

    ranked = sorted(merged.values(), key=lambda x: x["hybrid_score"], reverse=True)
    return ranked[:top_k]


def _extract_income_lakh(text: str) -> float | None:
    match = INCOME_RE.search(text)
    if not match:
        return None
    number = float(match.group(1))
    unit = (match.group(2) or "").lower()
    if unit in {"crore"}:
        return number * 100
    return number


def _extract_age_limits(text: str) -> tuple[int | None, int | None]:
    for min_age, max_age in AGE_RE.findall(text):
        if min_age and max_age:
            lo, hi = int(min_age), int(max_age)
            return min(lo, hi), max(lo, hi)
        if min_age:
            return int(min_age), None
    return None, None


def _extract_eligibility_signals(question: str, context: str) -> EligibilitySignals:
    q_income = _extract_income_lakh(question)
    q_min_age, _ = _extract_age_limits(question)
    c_income = _extract_income_lakh(context)
    c_min_age, c_max_age = _extract_age_limits(context)
    return EligibilitySignals(
        user_income_lakh=q_income,
        user_age=q_min_age,
        doc_income_limit_lakh=c_income,
        doc_min_age=c_min_age,
        doc_max_age=c_max_age,
    )


def _rule_based_verdict(signals: EligibilitySignals) -> tuple[str, list[str]]:
    reasons: list[str] = []
    verdict = "Possibly Eligible"

    if signals.doc_income_limit_lakh is not None and signals.user_income_lakh is not None:
        if signals.user_income_lakh > signals.doc_income_limit_lakh:
            verdict = "Not Eligible"
            reasons.append(
                f"User income {signals.user_income_lakh:.2f} lakh is above document limit {signals.doc_income_limit_lakh:.2f} lakh."
            )
        else:
            reasons.append(
                f"User income {signals.user_income_lakh:.2f} lakh is within document limit {signals.doc_income_limit_lakh:.2f} lakh."
            )

    if signals.doc_min_age is not None and signals.user_age is not None and signals.user_age < signals.doc_min_age:
        verdict = "Not Eligible"
        reasons.append(f"User age {signals.user_age} is below minimum age {signals.doc_min_age}.")

    if signals.doc_max_age is not None and signals.user_age is not None and signals.user_age > signals.doc_max_age:
        verdict = "Not Eligible"
        reasons.append(f"User age {signals.user_age} is above maximum age {signals.doc_max_age}.")

    if not reasons:
        verdict = "Insufficient Data"
        reasons.append("Could not extract enough structured income/age rules from question and cited context.")

    return verdict, reasons


def _validate_citations(question: str, chunks: list[dict]) -> list[dict]:
    q_tokens = set(_tokenize(question))
    validated: list[dict] = []

    for c in chunks:
        snippet = c["content"][:280]
        overlap = len(q_tokens.intersection(set(_tokenize(snippet))))
        if overlap == 0:
            continue
        validated.append(
            {
                "page": c["metadata"].get("page_number"),
                "section": c["metadata"].get("section_title"),
                "snippet": snippet,
                "overlap_score": overlap,
            }
        )

    return validated


def ask_question(document_id: str, question: str) -> dict:
    chunks = _hybrid_retrieve(document_id=document_id, question=question, top_k=4)
    context = "\n\n".join([f"[p{c['metadata'].get('page_number')}] {c['content']}" for c in chunks])

    signals = _extract_eligibility_signals(question=question, context=context)
    prompt = PROMPT.format(question=question, context=context, signals=signals)

    model_answer = SarvamService().generate_answer(prompt)
    rule_verdict, reasons = _rule_based_verdict(signals)

    citations = _validate_citations(question, chunks)
    if not citations:
        citations = [
            {
                "page": c["metadata"].get("page_number"),
                "section": c["metadata"].get("section_title"),
                "snippet": c["content"][:280],
                "overlap_score": 0,
            }
            for c in chunks[:1]
        ]

    eligibility_reasoning = {
        "extracted_signals": {
            "user_income_lakh": signals.user_income_lakh,
            "user_age": signals.user_age,
            "doc_income_limit_lakh": signals.doc_income_limit_lakh,
            "doc_min_age": signals.doc_min_age,
            "doc_max_age": signals.doc_max_age,
        },
        "rule_based_verdict": rule_verdict,
        "reasons": reasons,
    }

    final_answer = (
        f"{model_answer}\n\n"
        f"Eligibility reasoning: {rule_verdict}. "
        + " ".join(reasons)
    )

    confidence = 0.6 + (0.07 * len(citations))
    if rule_verdict == "Insufficient Data":
        confidence -= 0.15

    return {
        "answer": final_answer,
        "eligibility": rule_verdict if rule_verdict != "Possibly Eligible" else infer_eligibility(model_answer),
        "citations": citations,
        "confidence": round(max(0.2, min(0.95, confidence)), 2),
        "eligibility_reasoning": eligibility_reasoning,
    }


def infer_eligibility(answer: str) -> str:
    text = answer.lower()
    if "not eligible" in text:
        return "Not Eligible"
    if "likely eligible" in text:
        return "Likely Eligible"
    if "possibly" in text:
        return "Possibly Eligible"
    return "Insufficient Data"
