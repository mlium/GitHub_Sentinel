# subscriptions/subscription_manager.py

import json
from pathlib import Path
from typing import List, Optional
from config import SUBSCRIPTIONS_FILE

class SubscriptionManager:
    def __init__(self):
        self.file_path = SUBSCRIPTIONS_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保订阅文件存在"""
        if not self.file_path.exists():
            self.file_path.write_text('[]')
    
    def get_subscriptions(self) -> List[str]:
        """获取所有订阅"""
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def add_subscription(self, repo_url: str) -> str:
        """添加新的订阅"""
        # 标准化 repo_url 格式
        repo_url = self._normalize_repo_url(repo_url)
        
        subs = self.get_subscriptions()
        if repo_url in subs:
            return f"Repository {repo_url} is already subscribed."
        
        subs.append(repo_url)
        with open(self.file_path, 'w') as f:
            json.dump(subs, f, indent=2)
        
        return f"Successfully subscribed to {repo_url}"
    
    def remove_subscription(self, repo_url: str) -> str:
        """移除订阅"""
        repo_url = self._normalize_repo_url(repo_url)
        
        subs = self.get_subscriptions()
        if repo_url not in subs:
            return f"Repository {repo_url} is not in subscriptions."
        
        subs.remove(repo_url)
        with open(self.file_path, 'w') as f:
            json.dump(subs, f, indent=2)
        
        return f"Successfully unsubscribed from {repo_url}"
    
    def _normalize_repo_url(self, repo_url: str) -> str:
        """标准化仓库URL格式"""
        # 移除可能的 GitHub URL 前缀
        repo_url = repo_url.replace('https://github.com/', '')
        repo_url = repo_url.replace('http://github.com/', '')
        # 移除末尾的斜杠
        repo_url = repo_url.rstrip('/')
        return repo_url
