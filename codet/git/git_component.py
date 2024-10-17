import git
from datetime import datetime, timedelta
from collections import Counter
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

class GitAnalyzer:
    def __init__(self, repo_path, days=7):
        """
        Initializes the GitAnalyzer with the repository path and the number of days to analyze.

        :param repo_path: Path to the Git repository.
        :param days: Number of days to look back for commits. Defaults to 7.
        """
        self.repo_path = repo_path
        self.days = days
        # Open the Git repository at the specified path
        self.repo = git.Repo(repo_path)
        self.changed_files = []

    def analyze_commits(self):
        since_date = datetime.now() - timedelta(days=self.days)
        
        # Retrieve commits since the specified date, excluding merge commits
        commits = list(self.repo.iter_commits(since=since_date, no_merges=True))
        
        # Iterate over each commit to gather changed files
        for commit in commits:
            # Get the diff for each commit compared to its parent (or initial commit if no parent)
            diff = commit.diff(commit.parents[0] if commit.parents else None, create_patch=False)
            for diff_item in diff:
                if diff_item.a_path:  # Ensure that the file path exists
                    self.changed_files.append(diff_item.a_path)

    def display_changes(self):
        # Count how many times each file was changed
        file_change_count = Counter(self.changed_files)
        
        # Sort files by the number of changes in descending order
        sorted_files = file_change_count.most_common()
        
        # Calculate total number of changes for percentage calculation
        total_changes = sum(file_change_count.values())

        for file, count in sorted_files:
            change_percentage = (count / total_changes) * 100
            
            color = Fore.GREEN

            if change_percentage >= 10:
                color = Fore.RED  # High change percentage (>= 10%)
            elif 10 > change_percentage > 3:
                color = Fore.YELLOW  # Medium change percentage (> 3% and < 10%)

            print(f"{color}{count} {file}{Style.RESET_ALL}")