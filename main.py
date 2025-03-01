# main.py
import sys
import os
from dotenv import load_dotenv
from subscriptions.subscription_manager import SubscriptionManager
from updater.fetch_updates import fetch_updates
from notifier.notification_manager import send_notification

def handle_add_subscription(repo_url):
    manager = SubscriptionManager()
    result = manager.add_subscription(repo_url)
    print(result)

def handle_remove_subscription(repo_url):
    manager = SubscriptionManager()
    result = manager.remove_subscription(repo_url)
    print(result)

def handle_list_subscriptions():
    manager = SubscriptionManager()
    subs = manager.get_subscriptions()
    if subs:
        print("Current subscriptions:")
        for repo in subs:
            print(f"- {repo}")
    else:
        print("No subscriptions.")

def handle_update():
    """处理更新命令，获取更新并生成报告"""
    try:
        # 获取订阅列表
        subscription_manager = SubscriptionManager()
        subscriptions = subscription_manager.get_subscriptions()
        
        if not subscriptions:
            print("No subscriptions to update.")
            return
        
        # 获取更新并生成报告
        results = fetch_updates(subscriptions)
        
        # 处理结果
        for repo, result in results.items():
            if result['status'] == 'success':
                print(f"Successfully generated report for {repo}: {result['report_path']}")
                # 发送通知
                send_notification(f"已生成 {repo} 的每日报告", f"报告路径: {result['report_path']}")
            else:
                print(f"Failed to process {repo}: {result['error']}")
                send_notification(f"处理 {repo} 时出错", f"错误信息: {result['error']}")
    
    except Exception as e:
        error_msg = f"Error during update: {str(e)}"
        print(error_msg)
        send_notification("更新过程出错", error_msg)

def show_help():
    help_text = """
GitHub Sentinel v0.2 CLI Commands:
  add <repo_url>        Add a new repository subscription (format: owner/repo).
  remove <repo_url>     Remove an existing repository subscription.
  list                  List current repository subscriptions.
  update                Fetch updates for all subscriptions and generate daily reports.
  help                  Show this help message.
  exit                  Exit the tool.
"""
    print(help_text)

def process_command(command_line):
    parts = command_line.split()
    if not parts:
        return
    command = parts[0]
    args = parts[1:]
    
    if command == "add" and len(args) == 1:
        handle_add_subscription(args[0])
    elif command == "remove" and len(args) == 1:
        handle_remove_subscription(args[0])
    elif command == "list":
        handle_list_subscriptions()
    elif command == "update":
        handle_update()
    elif command == "help":
        show_help()
    elif command == "exit":
        print("Exiting GitHub Sentinel.")
        sys.exit(0)
    else:
        print("Unknown command. Type 'help' for available commands.")

def interactive_cli():
    # 加载环境变量
    load_dotenv()
    
    print("Welcome to GitHub Sentinel v0.2!")
    show_help()
    while True:
        try:
            command_line = input("$ ").strip()
            process_command(command_line)
        except KeyboardInterrupt:
            print("\nExiting GitHub Sentinel.")
            sys.exit(0)

if __name__ == "__main__":
    interactive_cli()
