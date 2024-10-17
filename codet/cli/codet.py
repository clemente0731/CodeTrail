# !/usr/bin/env python

import git
from pprint import pprint
from datetime import datetime, timedelta
from collections import Counter
from colorama import Fore, Style, init


HELLO_CODET = r"""
===========================================================================
---------------------------------codet-------------------------------------
 ██████╗ ██████╗ ██████╗ ███████╗    ████████╗██████╗  █████╗ ██╗██╗     
██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██║██║     
██║     ██║   ██║██║  ██║█████╗         ██║   ██████╔╝███████║██║██║     
██║     ██║   ██║██║  ██║██╔══╝         ██║   ██╔══██╗██╔══██║██║██║     
╚██████╗╚██████╔╝██████╔╝███████╗       ██║   ██║  ██║██║  ██║██║███████╗
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
 --------------------------------codet-------------------------------------
===========================================================================
"""


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
            # Check if the commit has parent commits
            if commit.parents:
                parent_commit = commit.parents[0]
                print("Commit message summary:", commit.summary)
                
                # Get the diff index between the current commit and its parent
                for diff in commit.diff(parent_commit, create_patch=True):
                    print("---------------------------------------->")
                    print(f"File: {diff.a_path}")
                    # Print the file diff if it exists, otherwise indicate no changes
                    print(f"File diff: {diff.diff.decode('utf-8') if diff.diff else 'N/A'}")
                    print("----------------------------------------<")

            # Get the diffs without creating a patch
            diffs = commit.diff(parent_commit, create_patch=False)
            for diff_item in diffs:
                if diff_item.a_path:  # Ensure that the file path exists
                    self.changed_files.append(diff_item.a_path)


    def display_changes(self):
        # Count how many times each file was changed
        file_change_count = Counter(self.changed_files)
        
        # Sort files by the number of changes in descending order
        sorted_files = file_change_count.most_common()
        
        # Calculate total number of changes for percentage calculation
        total_changes = sum(file_change_count.values())

        # Print the total number of changes
        print(f"{Fore.GREEN}Total changes: {total_changes}{Style.RESET_ALL}")
        
        for file, count in sorted_files:
            change_percentage = (count / total_changes) * 100
            
            color = Fore.GREEN

            if change_percentage >= 10:
                color = Fore.RED  # High change percentage (>= 10%)
            elif 10 > change_percentage > 3:
                color = Fore.YELLOW  # Medium change percentage (> 3% and < 10%)

            print(f"  {color}{count} {file}{Style.RESET_ALL}")

import argparse

def main():
    parser = argparse.ArgumentParser(description='Analyze commit history of a Git repository')
    parser.add_argument('--days', type=int, default=14, help='Number of days to look back for commits, defaults to 14 days')
    
    args = parser.parse_args()
    
    print(HELLO_CODET)
    git_analyzer = GitAnalyzer("./", args.days)
    git_analyzer.analyze_commits()
    git_analyzer.display_changes()

if __name__ == "__main__":
    main()
