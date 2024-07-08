from fastapi.testclient import TestClient
from .main import app
from .github_client import create_or_update_file
from .config import FILE_PATH

client = TestClient(app)

def test_create_or_update_post():
    # Define sample POST data
    slug = "sample-slug"
    post_data = {
        "title": "Sample Title",
        "description": "Sample Description",
        "draft": False,
        # "tags": ["tag1", "tag2"],
        "slug": slug,
        "content": "Sample content"
    }

    content = "---\n"
    for field, value in post_data.items():
        content += f"{field}: {value}\n"
    content += "---\n"
    content += post_data.get('content', '')

    # Simulate a POST request to your FastAPI endpoint with JSON data
    response = create_or_update_file(
        file_path=f"{FILE_PATH}{slug}.md",
        content=content,
    )

    assert "successfully" in response