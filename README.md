## Project Overview
Markdown CMS for Telegram enables users to manage their blog or website content directly from a Telegram bot. It is designed specifically for blogs where content is stored in markdown files within a Git repository. Users can create, update, and manage their markdown files seamlessly through a Telegram chat interface.

## Features
- Manage blog posts via Telegram.
- Customizable fields based on user requirements.
- Automatic markdown file generation.
- Stores markdown files in a specified Git repository.
     
## Configuration

### Repository Setup   
To store the markdown files, the bot requires access to a Git repository.    
You'll need to provide a personal access token with write permissions for the specific repository where the files will be stored.

Example `config.json`
```json
{
  "language": "en",
  "website_url": "https://example.com/",
  "repository": {
    "url": "https://github.com/your-username/your-repo",
    "branch": "main",
    "folder": "path/to/your/folder"
  },
  "telegram": {
    "allowed_usernames": []
  },
  "fields": {
    "title": {
      "alias": "Title",
      "required": true
    },
    "description": {
      "alias": "Description",
      "required": false
    },
    "draft": {
      "alias": "Draft",
      "required": false
    },
    "tags": {
      "alias": "Tags",
      "required": false
    },
    "slug": {
      "alias": "Slug",
      "required": true
    },
    "content": {
      "alias": "Content",
      "required": true
    }
  }
}
```

Please create a `.env` file at the root of the project.    
The Telegram token will be used to connect the server to your Telegram bot.      
The GitHub token will be used to push the generated markdown file to the provided repository. Ensure that your GitHub token has sufficient permissions to write to the specified repository.    
Support for more cloud Git repository managers is on the roadmap.     

```
TELEGRAM_TOKEN=your-telegram-token
GITHUB_TOKEN=your-github-token
```

## Field Management
Users can configure which fields they want the bot to manage.    
Each field can have an alias, which is useful for localization or simply making the field names more intuitive.

## Bot Commands
`/start`   
Initializes the bot and displays a welcome message along with the available commands.

`/newpost`    
Starts the process of creating a new blog post. The bot will prompt the user for each configured field.

`/editpost [slug]`    
Allows the user to edit an existing blog post. The bot will fetch the post based on the provided slug and prompt the user for each configured field.

`/deletepost [slug]`    
Deletes the specified blog post.

`/listposts`      
Displays a list of all blog posts with their titles and slugs.

## Example Interaction
User starts creating a new post:

```
User: /newpost
Bot: Please enter the Titre (title):
User: Lorem Ipsum
Bot: Please enter the Description (description):
User: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Bot: Please enter the Slug (slug):
User: lorem-ipsum-dolor
Bot: Please enter the Content (content):
User: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Bot: Here is the information you have entered:
- Title: Lorem Ipsum
- Description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Slug: lorem-ipsum-dolor
- Content: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Bot: Do you want to publish this post? (yes/no)
User: yes
Bot: Your post has been published successfully.
```
The bot then generates the markdown file with the provided information and commits it to the specified repository and folder path.

Generated markdown file based on the example interaction:
```md
---
title: Lorem Ipsum
description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
draft: ""
tags: ""
slug: lorem-ipsum-dolor
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
```

## Conclusion
Markdown CMS for Telegram provides a straightforward way to manage blog content using Telegram. By customizing the fields and their aliases, users can tailor the bot to their specific needs, ensuring a seamless content creation experience. Additionally, the integration with Git repositories ensures that content is stored securely and version-controlled.
