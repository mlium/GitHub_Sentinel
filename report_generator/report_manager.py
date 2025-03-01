# report_generator/report_manager.py
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from llm.deepseek_api import analyze_text

def save_daily_progress(repo_name: str, updates: Dict) -> str:
    """保存每日进展到markdown文件"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    repo_dir = data_dir / repo_name
    repo_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    file_path = repo_dir / f"{today}_raw.md"
    
    content = generate_markdown_content(repo_name, updates)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(file_path)

def generate_markdown_content(repo_name: str, updates: Dict) -> str:
    """生成markdown格式的内容"""
    today = datetime.now().strftime('%Y-%m-%d')
    content = [f"# {repo_name} 项目进展 ({today})\n"]
    
    # Issues部分
    content.append("## Issues 更新")
    for issue in updates.get('issues', []):
        content.append(f"- [{issue['title']}]({issue['url']}) "
                      f"(#{issue['number']}) - {issue['state']}")
    
    # PRs部分
    content.append("\n## Pull Requests 更新")
    for pr in updates.get('pull_requests', []):
        content.append(f"- [{pr['title']}]({pr['url']}) "
                      f"(#{pr['number']}) - {pr['state']}")
    
    return '\n'.join(content)

def generate_daily_report(repo_name: str, raw_data_path: str) -> str:
    """生成每日项目报告"""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    repo_dir = reports_dir / repo_name
    repo_dir.mkdir(exist_ok=True)
    
    # 读取原始数据
    with open(raw_data_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用 LLM 生成总结
    analysis = analyze_text(content)
    
    if not analysis['success']:
        raise Exception(f"Failed to analyze content: {analysis['error']}")
    
    # 保存报告
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = repo_dir / f"{today}_report.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# {repo_name} 项目日报 ({today})\n\n")
        f.write(analysis['summary'])
        f.write("\n\n## 原始数据\n")
        f.write(content)
    
    return str(report_path)
