import os

# GitHub API key (should be stored in a secure manner, like environment variables)
GITHUB_API_KEY = os.getenv('GITHUB_API_KEY', 'your-github-api-key')

# Notification configurations
NOTIFY_VIA_EMAIL = False
NOTIFY_VIA_SLACK = True
