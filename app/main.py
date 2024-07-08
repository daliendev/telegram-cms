from fastapi import FastAPI, HTTPException
from .github_client import create_or_update_file
from .config import FILE_PATH

app = FastAPI()

# Endpoint to create or update a markdown file
@app.post("/create-or-update-post/")
def create_or_update_post(data: dict):
    try:
        # Construct the file content dynamically based on the config file
        content = "---\n"
        for field, value in data.items():
            content += f"{field}: {value}\n"
        content += "---\n"
        content += data.get('content', '')

        # Define the file path
        file_path = f"{FILE_PATH}{data['slug']}.md"

        # Create or update the file in the repository
        create_or_update_file(file_path, content, data.get('commit_message', 'Updated file'))

        return {"message": "File created or updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with uvicorn app.main:app --reload