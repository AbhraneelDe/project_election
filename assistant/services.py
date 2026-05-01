"""
assistant/services.py
──────────────────────
Services for Gemini API interaction and fallback responses.
"""

import json
import requests
import logging
from typing import List, Dict, Any
from django.conf import settings
from .prompts import ELECTION_SYSTEM_PROMPT
from .constants import FALLBACK_RESPONSES

logger = logging.getLogger(__name__)

class GeminiService:
    """Service to interact with the Google Gemini 1.5 Flash API."""

    @staticmethod
    def get_reply(user_message: str, history: List[Dict[str, str]]) -> str:
        """
        Call Gemini API and return the response text.
        """
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key or api_key == "your_gemini_api_key_here":
            return FallbackService.get_response(user_message)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        try:
            contents = GeminiService._build_contents(user_message, history)
            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                },
                "safetySettings": [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            return GeminiService._extract_response_text(data)

        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API request failed: {e}")
            return "I'm having trouble connecting to my brain right now. Please try again in a moment."
        except Exception as e:
            logger.error(f"Unexpected error in GeminiService: {e}")
            return "An unexpected error occurred. Please try again."

    @staticmethod
    def _build_contents(user_message: str, history: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Construct the contents array for Gemini API."""
        contents = []

        # System Prompt (as first user turn fallback for v1beta)
        contents.append({
            "role": "user",
            "parts": [{"text": ELECTION_SYSTEM_PROMPT + "\n\nPlease acknowledge you understand your role."}]
        })
        contents.append({
            "role": "model",
            "parts": [{"text": "Understood! I'm ElectionGuide AI — your friendly, step-by-step guide to understanding elections."}]
        })

        # History (last 10 turns)
        for entry in history[-10:]:
            role = "user" if entry.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": entry.get("content", "")}]
            })

        # New user message
        contents.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        return contents

    @staticmethod
    def _extract_response_text(data: Dict[str, Any]) -> str:
        """Extract text from the Gemini API response JSON."""
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
        return "I'm sorry, I couldn't generate a response."


class FallbackService:
    """Service to provide keyword-based educational content."""

    @staticmethod
    def get_response(message: str) -> str:
        """
        Analyze the message and return a relevant educational snippet.
        """
        msg = message.lower()

        if any(w in msg for w in ["register", "registration", "sign up", "eligible"]):
            return FALLBACK_RESPONSES["registration"]
        if any(w in msg for w in ["electoral college", "electors", "electoral vote"]):
            return FALLBACK_RESPONSES["electoral_college"]
        if any(w in msg for w in ["primary", "caucus", "nomination"]):
            return FALLBACK_RESPONSES["primaries"]
        if any(w in msg for w in ["count", "counting", "certif", "result"]):
            return FALLBACK_RESPONSES["counting"]
        if any(w in msg for w in ["mail", "absentee", "mail-in", "postal"]):
            return FALLBACK_RESPONSES["mail_in"]
        if any(w in msg for w in ["id", "identification", "documents", "bring"]):
            return FALLBACK_RESPONSES["voter_id"]
        if any(w in msg for w in ["inaugurati", "january 20", "swear", "oath"]):
            return FALLBACK_RESPONSES["inauguration"]
        if any(w in msg for w in ["hello", "hi", "hey", "help", "start"]):
            return FALLBACK_RESPONSES["welcome"]

        return FALLBACK_RESPONSES["default"]
