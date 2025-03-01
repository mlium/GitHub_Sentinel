# config.py
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()  # 加载 .env 中的环境变量

# 基础目录配置
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
NOTIFICATIONS_DIR = BASE_DIR / "notifications"

# 确保必要的目录存在
for directory in [DATA_DIR, REPORTS_DIR, NOTIFICATIONS_DIR]:
    directory.mkdir(exist_ok=True)

# 订阅配置文件路径
SUBSCRIPTIONS_FILE = BASE_DIR / "subscriptions.json"

# GitHub API 配置
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 通知配置
NOTIFICATION_ENABLED = True

class Config:
    GITHUB_TOKEN = GITHUB_TOKEN
    DEEPSEEK_API_KEY = DEEPSEEK_API_KEY
    # 此处订阅信息暂存于内存，后续可扩展为持久化存储
    NOTIFY_METHOD = os.getenv("NOTIFY_METHOD", "email")
