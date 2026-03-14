from __future__ import annotations

from langchain.prompts import PromptTemplate

from app.services.sarvam_service import SarvamService
from app.services.vector_store_service import search_chunks

PROMPT = PromptTemplate.from_template(
    """
You explain Indian government schemes in simple language.
Use ONLY the provided context.
If context is insufficient, say 'Insufficient Data'.

Question: {question}
Context: {context}

Return a concise answer and include one eligibility verdict:
Likely Eligible / Possibly Eligible / Not Eligible / Insufficient Data
"""
)


def ask_question(document_id: str, question: str) -> dict:
    chunks = search_chunks(query=question, document_id=document_id, k=4)
    context = "\n\n".join([f"[page {c['metadata'].get('page_number')}] {c['content']}" for c in chunks])
    prompt = PROMPT.format(question=question, context=context)
    answer = SarvamService().generate_answer(prompt)
    return {
        "answer": answer,
        "eligibility": infer_eligibility(answer),
        "citations": [
            {
                "page": c["metadata"].get("page_number"),
                "section": c["metadata"].get("section_title"),
                "snippet": c["content"][:240],
            }
            for c in chunks
        ],
        "confidence": round(min(0.95, 0.55 + 0.08 * len(chunks)), 2),
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
