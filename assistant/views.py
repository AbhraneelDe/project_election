"""
assistant/views.py
──────────────────
Views for the Election Process Assistant.
- home(): landing page with timeline
- chat_page(): the interactive chat UI
- chat_api(): POST endpoint that queries Gemini and returns JSON
"""

import json
import logging
from typing import Dict, Any

from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .constants import TIMELINE_STEPS, SUGGESTED_QUESTIONS
from .services import GeminiService

logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    """Render the landing page with election timeline."""
    context = {
        "timeline_steps": TIMELINE_STEPS,
        "page_title": "Election Process Guide",
    }
    return render(request, 'assistant/home.html', context)


def chat_page(request: HttpRequest) -> HttpResponse:
    """Render the interactive AI chat interface."""
    context = {
        "page_title": "Chat with ElectionGuide",
        "suggested_questions": SUGGESTED_QUESTIONS,
    }
    return render(request, 'assistant/chat.html', context)


@csrf_exempt
def chat_api(request: HttpRequest) -> JsonResponse:
    """
    POST /api/chat/
    Body: { "message": "user's question", "history": [...] }
    Returns: { "reply": "assistant's response" }
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed."}, status=405)

    try:
        body: Dict[str, Any] = json.loads(request.body)
        user_message: str = body.get("message", "").strip()
        history: list = body.get("history", [])

        if not user_message:
            return JsonResponse({"error": "Message is required."}, status=400)

        # Delegate API logic to the GeminiService
        reply = GeminiService.get_reply(user_message, history)

        return JsonResponse({"reply": reply})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)
    except Exception as e:
        logger.error(f"Chat API error: {e}")
        return JsonResponse({"error": "An internal error occurred. Please try again."}, status=500)
