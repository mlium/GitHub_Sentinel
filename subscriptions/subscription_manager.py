class SubscriptionManager:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, repo_url):
        if repo_url not in self.subscriptions:
            self.subscriptions.append(repo_url)
            return f"Repository {repo_url} added."
        return f"Repository {repo_url} already exists in the list."

    def remove_subscription(self, repo_url):
        if repo_url in self.subscriptions:
            self.subscriptions.remove(repo_url)
            return f"Repository {repo_url} removed."
        return f"Repository {repo_url} not found."

    def get_subscriptions(self):
        return self.subscriptions
