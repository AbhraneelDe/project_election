from django.test import TestCase, RequestFactory
from django.urls import reverse
from .views import home, chat_page, chat_api
from .services import FallbackService, GeminiService
from .constants import FALLBACK_RESPONSES
import json

class AssistantViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home_view(self):
        """Test that the home page renders correctly."""
        request = self.factory.get(reverse('home'))
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_chat_page_view(self):
        """Test that the chat page renders correctly."""
        request = self.factory.get(reverse('chat'))
        response = chat_page(request)
        self.assertEqual(response.status_code, 200)

    def test_chat_api_invalid_method(self):
        """Test that GET request to chat API returns 405."""
        request = self.factory.get(reverse('chat_api'))
        response = chat_api(request)
        self.assertEqual(response.status_code, 405)

    def test_chat_api_missing_message(self):
        """Test that missing message returns 400."""
        request = self.factory.post(
            reverse('chat_api'),
            data=json.dumps({"history": []}),
            content_type='application/json'
        )
        response = chat_api(request)
        self.assertEqual(response.status_code, 400)


class ServicesTestCase(TestCase):
    def test_fallback_service_registration(self):
        """Test registration keywords return correct fallback."""
        reply = FallbackService.get_response("How do I register?")
        self.assertEqual(reply, FALLBACK_RESPONSES["registration"])

    def test_fallback_service_electoral(self):
        """Test electoral college keywords return correct fallback."""
        reply = FallbackService.get_response("Explain the electoral college")
        self.assertEqual(reply, FALLBACK_RESPONSES["electoral_college"])

    def test_fallback_service_default(self):
        """Test unknown input returns default fallback."""
        reply = FallbackService.get_response("What is the meaning of life?")
        self.assertEqual(reply, FALLBACK_RESPONSES["default"])

    def test_gemini_service_extract_text(self):
        """Test extracting text from mock API response."""
        mock_data = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "Hello world"}]
                    }
                }
            ]
        }
        text = GeminiService._extract_response_text(mock_data)
        self.assertEqual(text, "Hello world")
