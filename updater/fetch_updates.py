# updater/fetch_updates.py
from datetime import datetime
from typing import Dict, List
from updater.github_api import get_repo_updates
from report_generator.report_manager import save_daily_progress, generate_daily_report

def fetch_updates(repo_list: List[str]) -> Dict[str, str]:
    """获取所有订阅仓库的更新并生成报告"""
    results = {}
    
    for repo in repo_list:
        try:
            # 获取仓库更新
            updates = get_repo_updates(repo)
            
            # 保存原始进展数据
            raw_data_path = save_daily_progress(repo, updates)
            
            # 生成每日报告
            report_path = generate_daily_report(repo, raw_data_path)
            
            results[repo] = {
                'status': 'success',
                'report_path': report_path
            }
        except Exception as e:
            results[repo] = {
                'status': 'error',
                'error': str(e)
            }
    
    return results
