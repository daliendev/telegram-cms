import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from config.json
def load_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
    return config

# Get GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Load configuration from config.json
config = load_config()

# Extract repository details from config.json
REPO_URL = config['repository']['url']
parsed_url = urlparse(REPO_URL)
path_parts = parsed_url.path.strip('/').split('/')
REPO_OWNER = path_parts[0]  # Owner is the first part of the path
REPO_NAME = path_parts[1]   # Repo name is the second part of the path

REPO_BRANCH = config['repository']['branch']
REPO_FOLDER = config['repository']['folder']

# Define FILE_PATH based on repository folder
FILE_PATH = REPO_FOLDER + '/'  # Ensure trailing slash for folder path
