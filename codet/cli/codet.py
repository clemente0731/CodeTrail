# !/usr/bin/env python

import argparse
from codet.git.git_component import GitAnalyzer

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


def main():
    parser = argparse.ArgumentParser(
        description=f"Analyze commit history of a Git repository"
    )
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        default=7,
        help="Number of days to look back for commits (default: 7 days)",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        default="",
        help="Search for a keyword in the current commit diff (default: empty)",
    )
    parser.add_argument(
        "-g",
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode (default: off)",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="nvidia/llama-3.1-nemotron-70b-instruct",
        help="Specify the model to use (default: nvidia/llama-3.1-nemotron-70b-instruct), please refer to https://build.nvidia.com/nim",
    )
    parser.add_argument(
        "-u",
        "--base_url",
        type=str,
        default="https://integrate.api.nvidia.com/v1",
        help="Specify the base URL for openai client (default: https://integrate.api.nvidia.com/v1)",
    )
    args = parser.parse_args()

    # validate days argument
    if args.days < 1:
        parser.error("The number of days must be a positive integer.")

    print(HELLO_CODET)
    git_analyzer = GitAnalyzer("./", args)
    git_analyzer.analyze_commits()
    git_analyzer.display_changes()


if __name__ == "__main__":
    main()
