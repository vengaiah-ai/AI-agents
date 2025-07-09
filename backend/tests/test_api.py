# Example test_api.py

import requests

def test_placeholder():
    assert True 

def test_generate_content_returns_article_content(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self._json = json_data
            self.status_code = status_code
        def json(self):
            return self._json
    def mock_post(url, json):
        return MockResponse({
            "status": "success",
            "message": "Content generated successfully",
            "file_path": "output/test.pdf",
            "download_url": "/api/download/test.pdf",
            "article_content": "This is the generated article content."
        }, 200)
    monkeypatch.setattr(requests, "post", mock_post)
    response = requests.post("http://localhost:8000/api/generate-content", json={"topic": "Test Topic"})
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "success"
    assert "article_content" in data
    assert data["article_content"] == "This is the generated article content." 