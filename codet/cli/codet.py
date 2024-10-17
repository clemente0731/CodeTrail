# !/usr/bin/env python

import git
from pprint import pprint
from datetime import datetime, timedelta
from collections import Counter
from colorama import Fore, Style, init
import argparse
import csv


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
    def __init__(self, repo_path, args):
        """
        Initializes the GitAnalyzer with the repository path and the number of days to analyze.

        :param repo_path: Path to the Git repository.
        :param days: Number of days to look back for commits. Defaults to 7.
        """
        self.repo_path = repo_path
        self.days = args.days
        self.keyword = args.keyword
        self.debug = args.debug
        # Open the Git repository at the specified path
        self.repo = git.Repo(repo_path)
        self.changed_files = []
        # Stores commit records in the format {commit_id: {commit_message: commit message, 
        # commit_date: commit date, commit_author: commit author, commit_email: 
        # commit email, commit_diffs: commit diffs, commit_diff_count: number of changed files,
        # commit_diff_summary: summary of diffs, commit_diff_files: list of changed files}}
        self.commit_records = {}  

    def analyze_commits(self):
        since_date = datetime.now() - timedelta(days=self.days)
        
        # Retrieve commits since the specified date, excluding merge commits
        commits = list(self.repo.iter_commits(since=since_date, no_merges=True))
        
        # Iterate over each commit to gather changed files
        for commit in commits:
            # Check if the commit has parent commits
            if commit.parents:
                parent_commit = commit.parents[0]
                
                commit_summary = commit.message.splitlines()[0]
                commit_hexsha = commit.hexsha
                commit_date = commit.committed_datetime
                commit_author = commit.author.name 
                commit_email = commit.author.email
                commit_message = commit.message
                commit_diffs = commit.diff(parent_commit, create_patch=True)
                commit_diff_count = len(commit_diffs)
                commit_diff_summary = f"{commit_diff_count} files changed"  # 简化差异摘要
                commit_diff_files = [diff.a_path for diff in commit_diffs]


                print(f"{Fore.BLUE}Commit Summary: {commit_summary:<50} (Commit ID: {commit_hexsha}){Style.RESET_ALL}")


                # this section gathers the diffs of the commit and checks for a keyword in the diffs.
                diffs_txt = ""
                for diff in commit_diffs:
                    diffs_txt += f"COMMIT MESSAGE: {commit_message}"
                    diffs_txt += f"COMMIT MODIFIED FILE NAME: {diff.a_path}"
                    modified_content = diff.diff.decode('utf-8') if diff.diff else 'NO CHANGES'
                    diffs_txt += f"COMMIT MODIFIED CONTENT: {modified_content}"

                ###########################
                ###   commit records   ####
                ###########################
                # # Check if a keyword is provided for searching in the diffs
                if self.keyword and self.keyword in diffs_txt:
                    print(f"{Fore.RED} keyword '{self.keyword}' found in diff: {self.keyword}{Style.RESET_ALL}")
                    self.commit_records[commit_hexsha] = {
                        'commit_message': commit_message,
                        'commit_date': commit_date,
                        'commit_email': commit_email,
                        'commit_diffs': diffs_txt.strip(),
                    }
                elif not self.keyword:
                    self.commit_records[commit_hexsha] = {
                        'commit_message': commit_message,
                        'commit_date': commit_date,
                        'commit_email': commit_email,
                        'commit_diffs': diffs_txt.strip(),
                    }



                #######################################
                ###  Integrate LLM AI for analysis ####
                #######################################
                import os
                from openai import OpenAI


                # Create OpenAI client
                client = OpenAI(
                    base_url="https://integrate.api.nvidia.com/v1",
                    api_key=os.environ['NVIDIA_API_KEY']
                )

                import time

                start_time = time.time()  # Record start time
                preliminary_prompt = "where is a bunch of git diff.you are the absolute expert of the entire project. Please help me analyze it:"
                diff = str(self.commit_records)
                full_prompt = preliminary_prompt + diff

                print("Analyzing commit records...")  # Print prompt message
                completion = client.chat.completions.create(
                    model="meta/llama-3.1-405b-instruct",
                    messages=[{"role": "user", "content": full_prompt}],
                    temperature=0.5,
                    top_p=0.7,
                    max_tokens=1024,
                    stream=True
                )

                reply = f"Hello "
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        reply += chunk.choices[0].delta.content
                
                print(reply)
                end_time = time.time()  # Record end time
                print(f"Analysis completed, took {end_time - start_time:.2f} seconds")  # Print elapsed time
                ###########################
                ###  debug && dump csv ####
                ###########################
                if self.debug:
                    print("---------------------------------------->")
                    print(f"COMMIT ID: {commit_hexsha}")
                    # print(f"COMMIT SUMMARY: {commit_summary}")
                    # print(f"DATE: {commit_date}")
                    # print(f"AUTHOR: {commit_author}")
                    # print(f"EMAIL: {commit_email}")
                    # print(f"DIFF COUNT: {commit_diff_count}")
                    # print(f"DIFF SUMMARY: {commit_diff_summary}")
                    # print(f"CHANGED FILES: {commit_diff_files}")
                    
                    for diff in commit_diffs:
                        modified_content = diff.diff.decode('utf-8') if diff.diff else 'NO CHANGES'
                        print(f"COMMIT MESSAGE: {commit_message}")
                        print(f"COMMIT MODIFIED FILE NAME: {diff.a_path}")
                        print(f"COMMIT MODIFIED CONTENT: {modified_content}")
                        print("----------------------------------------<")
                    
                    # Attempting to write commit records to a CSV file named 'commit_records.csv'
                    try:
                        print("Attempting to write commit records to 'commit_records.csv'...")
                        with open('commit_records.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            # Iterating through each commit record to write to the CSV
                            for commit_id, record in self.commit_records.items():
                                writer.writerow([commit_id, record])
                        print("Successfully wrote commit records to 'commit_records.csv'.")
                    except Exception as e:
                        # Handling any exceptions that occur during the file writing process
                        print(f"An error occurred while writing to 'commit_records.csv': {e}")

            
            ###########################
            ###  hotspot analysis  ####
            ###########################
            # Get the diffs without creating a patch
            diffs = commit.diff(parent_commit, create_patch=False)
            for diff_item in diffs:
                if diff_item.a_path:  # Ensure that the file path exists
                    self.changed_files.append(diff_item.a_path)  # Count changed files for hotspot analysis


    def display_changes(self):
        # Count how many times each file was changed
        file_change_count = Counter(self.changed_files)
        
        # Sort files by the number of changes in descending order
        sorted_files = file_change_count.most_common()
        
        # Calculate total number of changes for percentage calculation
        total_changes = sum(file_change_count.values())

        # Print the total number of changes
        print(f"\n{Fore.GREEN} Total hotspot changes detected: {total_changes}{Style.RESET_ALL}")
        
        for file, count in sorted_files:
            change_percentage = (count / total_changes) * 100
            
            color = Fore.GREEN

            if change_percentage >= 10:
                color = Fore.RED  # High change percentage (>= 10%)
            elif 10 > change_percentage > 3:
                color = Fore.YELLOW  # Medium change percentage (> 3% and < 10%)

            print(f"  {color}{count} {file}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(description='Analyze commit history of a Git repository')
    parser.add_argument('-d', '--days', type=int, default=7, help='Number of days to look back for commits, defaults to 14 days')
    parser.add_argument('-k', '--keyword', type=str, default='', help='Search for a keyword in the current commit diff, default is empty')
    parser.add_argument('--debug', action='store_true', default=False, help='Enable debug mode (default is off)')
    args = parser.parse_args()
    
    print(HELLO_CODET)
    git_analyzer = GitAnalyzer("./", args)
    git_analyzer.analyze_commits()
    git_analyzer.display_changes()

if __name__ == "__main__":
    main()
