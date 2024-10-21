# CodeTrail Codet

## Overview
`Codet` is a command-line tool for analyzing Git commit history. It helps users examine commit records, analyze code changes, and leverage AI for deeper insights.

## Features
- Analyze recent commit records, defaulting to the past 7 days.
- Search for keywords in commit diffs.
- Support for optional AI analysis via API.
- Code hotspot analysis to identify frequently modified areas.

## Usage

### Command Line Arguments
```bash
usage: codet [-h] [-d DAYS] [-k KEYWORD] [-g] [-m MODEL] [-t API_TOKEN] [-u BASE_URL]
```

- `-d`, `--days`: 
  - Number of days to look back for commits (default: 7 days).
  
- `-k`, `--keyword`: 
  - Search for a keyword in the current commit diff (default: empty).

- `-g`, `--debug`: 
  - Enable debug mode (default: off).

- `-m`, `--model`: 
  - Specify the model to use (default: `meta/llama-3.2-3b-instruct`).
  
- `-t`, `--api-token`: 
  - API token (if not set or incorrectly configured, AI analysis is skipped).

- `-u`, `--base_url`: 
  - Specify the base URL for the OpenAI client (default: `https://integrate.api.nvidia.com/v1`).

### Example
```bash
cd <some_git_repo_dir>

codet 

codet -k "bug fix"

codet -k "bug fix" -t "your_api_token"

codet -k "bug fix" -t "your_api_token" -m "nvidia/llama-3.1-nemotron-70b-instruct"

```

## Warning
If the API token is not set or incorrectly configured, AI analysis will be skipped.

## License
MIT License.

## Contact Us
If you have any questions, please contact the developer or ask in the project page.
```