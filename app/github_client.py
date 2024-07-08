from github import Github, Auth
from .config import GITHUB_TOKEN, REPO_NAME, REPO_OWNER

# Initialize GitHub client
github_client = Github(auth=Auth.Token(GITHUB_TOKEN))

def create_or_update_file(file_path, content, commit_message = 'Default Commit Message'):
    try:
        repo = github_client.get_repo(f'{REPO_OWNER}/{REPO_NAME}')
        
        try:
            # Check if the file already exists
            contents = repo.get_contents(file_path)
            # If it exists, update the file
            repo.update_file(contents.path, commit_message, content, contents.sha)
            return f"File '{file_path}' updated successfully."
        except Exception as e:
            # If the file does not exist, create a new file
            repo.create_file(file_path, commit_message, content)
            return f"File '{file_path}' created successfully."
    except Exception as e:
        return f"Error creating or updating file: {e}"