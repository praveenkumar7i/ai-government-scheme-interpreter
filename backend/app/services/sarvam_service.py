from __future__ import annotations

import httpx

from app.core.config import settings


class SarvamService:
    def __init__(self) -> None:
        self.api_key = settings.sarvam_api_key
        self.base_url = settings.sarvam_base_url.rstrip("/")

    def generate_answer(self, prompt: str) -> str:
        if not self.api_key:
            return (
                "Insufficient Data: Sarvam API key not configured. "
                "Configure SARVAM_API_KEY to enable model-generated answers."
            )

        payload = {"prompt": prompt, "model": "sarvam-m"}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with httpx.Client(timeout=30) as client:
            response = client.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        return data.get("text") or data.get("output", "Insufficient Data")

    def translate(self, text: str, target_language: str) -> str:
        if not self.api_key:
            return text

        payload = {"text": text, "source_language": "en", "target_language": target_language}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with httpx.Client(timeout=30) as client:
            response = client.post(f"{self.base_url}/v1/translate", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        return data.get("translated_text", text)
