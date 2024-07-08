from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_or_update_post():
    # Define sample POST data
    post_data = {
        "title": "Sample Title",
        "description": "Sample Description",
        "draft": False,
        # "tags": ["tag1", "tag2"],
        "slug": "sample-slug",
        "content": "Sample content update"
    }

    # Simulate a POST request to your FastAPI endpoint with JSON data
    response = client.post("/create-or-update-post/", json=post_data)

    # Assert the response status code
    assert response.status_code == 200
    
    # Assert the response content
    assert response.json() == {'message': 'File created or updated successfully.'}