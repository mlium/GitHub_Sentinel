import sys
from subscriptions.subscription_manager import SubscriptionManager
from updater.fetch_updates import fetch_updates
from notifier.notification_manager import NotificationManager
from report_generator.report_manager import ReportManager

def handle_add_subscription(repo_url):
    subscription_manager = SubscriptionManager()
    result = subscription_manager.add_subscription(repo_url)
    print(f"Added repository: {repo_url}")

def handle_remove_subscription(repo_url):
    subscription_manager = SubscriptionManager()
    result = subscription_manager.remove_subscription(repo_url)
    print(f"Removed repository: {repo_url}")

def handle_update_subscriptions():
    subscription_manager = SubscriptionManager()
    notification_manager = NotificationManager()
    report_manager = ReportManager()
    
    # 获取订阅仓库并更新
    subscriptions = subscription_manager.get_subscriptions()
    for repo_url in subscriptions:
        fetch_updates(repo_url)  # 即时抓取更新
    # 发送通知
    notification_manager.send_daily_notifications()
    # 生成报告
    report_manager.generate_daily_report()
    print("Updates completed and notifications sent.")

def handle_list_subscriptions():
    subscription_manager = SubscriptionManager()
    subscriptions = subscription_manager.get_subscriptions()
    if subscriptions:
        print("\nCurrent subscriptions:")
        for repo in subscriptions:
            print(repo)
    else:
        print("\nNo active subscriptions.")

def show_help():
    print("""
GitHub Sentinel - A tool for managing GitHub repository subscriptions

Usage:
  add <repository-url>         Add a new GitHub repository to track
  remove <repository-url>      Remove a GitHub repository from tracking
  update                      Fetch updates for all subscribed repositories and send notifications
  list                        List all currently subscribed repositories
  help                        Show this help message
  exit                        Exit the tool
""")

def process_command(command):
    if command[0] == "add" and len(command) == 2:
        handle_add_subscription(command[1])
    elif command[0] == "remove" and len(command) == 2:
        handle_remove_subscription(command[1])
    elif command[0] == "update" and len(command) == 1:
        handle_update_subscriptions()
    elif command[0] == "list" and len(command) == 1:
        handle_list_subscriptions()
    elif command[0] == "help" and len(command) == 1:
        show_help()
    elif command[0] == "exit" and len(command) == 1:
        print("Exiting GitHub Sentinel.")
        sys.exit(0)
    else:
        print("Unknown command. Type 'help' for available commands.")

def interactive_cli():
    print("Welcome to GitHub Sentinel! Type 'help' for available commands.")
    while True:
        try:
            # 等待用户输入命令
            command_input = input("\n$ ").strip()
            if command_input:
                command = command_input.split()
                process_command(command)
        except KeyboardInterrupt:
            print("\nExiting GitHub Sentinel.")
            sys.exit(0)

def main():
    # 启动交互式 CLI
    interactive_cli()

if __name__ == "__main__":
    main()
