import pytest
import json
from django.urls import reverse

from assistant.views import home, chat_page

@pytest.mark.django_db
def test_home_view(rf):
    """Test that the home page renders correctly."""
    request = rf.get(reverse('home'))
    response = home(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_chat_page_view(rf):
    """Test that the chat page renders correctly."""
    request = rf.get(reverse('chat'))
    response = chat_page(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_chat_api_invalid_method(client):
    """Test that GET request to chat API returns 405."""
    url = reverse('chat_api')
    response = client.get(url)
    assert response.status_code == 405

@pytest.mark.django_db
def test_chat_api_missing_message(client):
    """Test that missing message returns 400."""
    url = reverse('chat_api')
    response = client.post(
        url,
        data=json.dumps({"history": []}),
        content_type='application/json'
    )
    assert response.status_code == 400

@pytest.mark.django_db
def test_chat_api_success(client, mocker):
    """Test successful chat API response with mocked GeminiService."""
    mock_reply = mocker.patch('assistant.services.GeminiService.get_reply')
    mock_reply.return_value = "Mocked Response"
    
    url = reverse('chat_api')
    payload = {
        "message": "Hello",
        "history": []
    }
    response = client.post(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['reply'] == "Mocked Response"

@pytest.mark.django_db
def test_chat_api_invalid_json(client):
    """Test that invalid JSON returns 400."""
    url = reverse('chat_api')
    response = client.post(
        url,
        data="not a json",
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json()['error'] == "Invalid JSON body."

@pytest.mark.django_db
def test_chat_api_unexpected_exception(rf, mocker):
    """Test that unexpected exceptions return 500."""
    from assistant.views import chat_api
    mocker.patch('assistant.services.GeminiService.get_reply', side_effect=Exception("Fatal Error"))
    request = rf.post(
        reverse('chat_api'),
        data=json.dumps({"message": "hi"}),
        content_type='application/json'
    )
    response = chat_api(request)
    assert response.status_code == 500
    assert "error" in json.loads(response.content)
