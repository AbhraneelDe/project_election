"""
assistant/services.py
──────────────────────
Services for Gemini API interaction and fallback responses.
"""

import logging
import google.generativeai as genai
from typing import List, Dict, Any
from django.conf import settings
from .prompts import ELECTION_SYSTEM_PROMPT
from .constants import FALLBACK_RESPONSES

logger = logging.getLogger(__name__)

class GeminiService:
    """Service to interact with the Google Gemini 1.5 Flash API using the official SDK."""

    @staticmethod
    def get_reply(user_message: str, history: List[Dict[str, str]]) -> str:
        """
        Call Gemini API using the SDK and return the response text.
        """
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key or api_key == "your_gemini_api_key_here":
            return FallbackService.get_response(user_message)

        try:
            genai.configure(api_key=api_key)
            
            # Initialize model with system instructions and grounding tools
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=ELECTION_SYSTEM_PROMPT,
                tools=[{'google_search_retrieval': {}}] # Enable Google Search Grounding
            )

            # Convert history to SDK format
            chat_history = GeminiService._convert_history(history)
            
            # Start chat session
            chat = model.start_chat(history=chat_history)
            
            # Generate response
            generation_config = genai.types.GenerationConfig(
                temperature=0.3,
                top_p=0.95,
                top_k=40,
                max_output_tokens=1024,
            )
            
            response = chat.send_message(
                user_message,
                generation_config=generation_config,
                safety_settings={
                    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
            )

            if response.text:
                logger.info(f"Gemini success: {len(response.text)} chars returned.")
                return response.text
            
            logger.warning("Gemini returned empty text response.")
            return "I'm sorry, I couldn't generate a response."

        except Exception as e:
            logger.error(f"Gemini SDK Error: {e}")
            # Fallback to local response if API fails
            return FallbackService.get_response(user_message)

    @staticmethod
    def _convert_history(history: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Convert standard history format to Google SDK format."""
        converted = []
        # Last 10 turns for context
        for entry in history[-10:]:
            role = "user" if entry.get("role") == "user" else "model"
            converted.append({
                "role": role,
                "parts": [entry.get("content", "")]
            })
        return converted


class FallbackService:
    """Service to provide keyword-based educational content."""

    @staticmethod
    def get_response(message: str) -> str:
        """
        Analyze the message and return a relevant educational snippet.
        """
        import re
        msg = message.lower()
        
        def has_any(keywords):
            for kw in keywords:
                if kw == "id":
                    if re.search(r'\bid\b', msg): return True
                elif kw in msg:
                    return True
            return False

        if has_any(["register", "registration", "sign up", "eligible"]):
            return FALLBACK_RESPONSES["registration"]
        if has_any(["electoral college", "electors", "electoral vote"]):
            return FALLBACK_RESPONSES["electoral_college"]
        if has_any(["primary", "caucus", "nomination", "primaries"]):
            return FALLBACK_RESPONSES["primaries"]
        if has_any(["count", "counting", "certif", "result"]):
            return FALLBACK_RESPONSES["counting"]
        if has_any(["mail", "absentee", "mail-in", "postal"]):
            return FALLBACK_RESPONSES["mail_in"]
        # Special handling for voter ID keywords
        if has_any(["voter id", "identification", "documents"]) or re.search(r'\bid\b', msg):
            return FALLBACK_RESPONSES["voter_id"]
        if has_any(["inaugurati", "january 20", "swear", "oath"]):
            return FALLBACK_RESPONSES["inauguration"]
        if has_any(["hello", "hi", "hey", "help", "start"]):
            return FALLBACK_RESPONSES["welcome"]

        return FALLBACK_RESPONSES["default"]
