from fastapi.testclient import TestClient
import pytest
from ..main import app
from .github_client import list_files
from ..config import REPO_CONTENT_FOLDER

client = TestClient(app)

def test_list_files():
    response = list_files(file_path=REPO_CONTENT_FOLDER)
    
    assert not isinstance(response, Exception), f"Failed to list files: {response}"

    if response:
        filepath = response[0]
        assert REPO_CONTENT_FOLDER in filepath, f"Expected '{REPO_CONTENT_FOLDER}' in filepath, got '{filepath}'"
    else:
        assert False, "No files returned"

# Run the tests
if __name__ == '__main__':
    pytest.main()
    