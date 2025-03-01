# updater/github_api.py
import requests
from datetime import datetime
from typing import Dict
from github import Github
import os

def fetch_issues_and_prs(repo_url, token):
    """
    Fetch issues and pull requests from a GitHub repository.
    """
    # 假设 repo_url 格式为 "https://github.com/owner/repo"
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]
    
    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    prs_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    headers = {"Authorization": f"token {token}"}
    
    issues_resp = requests.get(issues_url, headers=headers)
    prs_resp = requests.get(prs_url, headers=headers)
    
    if issues_resp.status_code == 200 and prs_resp.status_code == 200:
        issues = issues_resp.json()
        prs = prs_resp.json()
        return issues, prs
    else:
        raise Exception(f"Failed to fetch issues/PRs for {repo_url}")

def get_repo_updates(repo_name: str) -> Dict:
    """
    获取GitHub仓库的更新信息
    
    Args:
        repo_name: 仓库名称，格式为 "owner/repo"
        
    Returns:
        Dict 包含 issues 和 pull requests 的更新信息
    """
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN not found in environment variables")
    
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    today = datetime.now().date()
    
    # 获取今日的 issues
    issues = []
    for issue in repo.get_issues(state='all', since=today):
        issues.append({
            'number': issue.number,
            'title': issue.title,
            'state': issue.state,
            'created_at': issue.created_at,
            'updated_at': issue.updated_at,
            'url': issue.html_url
        })

    # 获取今日的 PRs
    prs = []
    for pr in repo.get_pulls(state='all', sort='updated'):
        if pr.updated_at.date() >= today:
            prs.append({
                'number': pr.number,
                'title': pr.title,
                'state': pr.state,
                'created_at': pr.created_at,
                'updated_at': pr.updated_at,
                'url': pr.html_url
            })

    return {
        'issues': issues,
        'pull_requests': prs
    }
