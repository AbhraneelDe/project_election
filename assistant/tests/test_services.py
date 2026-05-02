import pytest
from unittest.mock import MagicMock
from assistant.services import GeminiService, FallbackService
from assistant.constants import FALLBACK_RESPONSES

def test_fallback_service_registration():
    """Test registration keywords return correct fallback."""
    reply = FallbackService.get_response("How do I register?")
    assert reply == FALLBACK_RESPONSES["registration"]

def test_fallback_service_electoral():
    """Test electoral college keywords return correct fallback."""
    reply = FallbackService.get_response("Explain the electoral college")
    assert reply == FALLBACK_RESPONSES["electoral_college"]

def test_fallback_service_default():
    """Test unknown input returns default fallback."""
    reply = FallbackService.get_response("What is the meaning of life?")
    assert reply == FALLBACK_RESPONSES["default"]

def test_gemini_service_fallback_on_missing_key(settings):
    """Test GeminiService falls back when API key is not configured."""
    settings.GEMINI_API_KEY = "your_gemini_api_key_here"
    reply = GeminiService.get_reply("hello", [])
    assert reply == FALLBACK_RESPONSES["welcome"]

def test_gemini_service_convert_history():
    """Test history conversion to SDK format."""
    history = [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"}
    ]
    converted = GeminiService._convert_history(history)
    assert len(converted) == 2
    assert converted[0]["role"] == "user"
    assert converted[1]["role"] == "model"
    assert converted[0]["parts"] == ["hi"]

def test_gemini_service_sdk_call_success(mocker, settings):
    """Test successful SDK interaction with mocking."""
    settings.GEMINI_API_KEY = "valid_key"
    
    # Mock genai.configure
    mock_configure = mocker.patch('google.generativeai.configure')
    
    # Mock GenerativeModel
    mock_model_class = mocker.patch('google.generativeai.GenerativeModel')
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    # Mock chat and response
    mock_chat = MagicMock()
    mock_model_instance.start_chat.return_value = mock_chat
    
    mock_response = MagicMock()
    mock_response.text = "Hello from AI"
    mock_chat.send_message.return_value = mock_response
    
    reply = GeminiService.get_reply("hi", [])
    
    assert reply == "Hello from AI"
    mock_configure.assert_called_once_with(api_key="valid_key")
    mock_model_instance.start_chat.assert_called_once()

def test_gemini_service_sdk_error_fallback(mocker, settings):
    """Test that SDK errors trigger the FallbackService."""
    settings.GEMINI_API_KEY = "valid_key"
    mocker.patch('google.generativeai.configure', side_effect=Exception("API Error"))
    
    reply = GeminiService.get_reply("How to register?", [])
    assert reply == FALLBACK_RESPONSES["registration"]
