#!/bin/bash

set -euo pipefail

# USAGE: forma.sh - formats modified Python files using ruff

# function to print messages in color
print_message() {
    local color="$1"
    shift
    echo -e "\033[${color}m$*\033[0m"
}

# check if ruff is installed
if ! command -v ruff &> /dev/null; then
    print_message "31" "ruff is not installed, attempting to install..."
    
    # try to install ruff using pip
    if pip install ruff; then
        print_message "32" "ruff installed successfully!"
    else
        print_message "31" "failed to install ruff, please install it manually."
        exit 1
    fi
else
    print_message "32" "ruff is installed, version: $(ruff --version)"
fi

# get modified Python files (incremental formatting)
modified_files=$(git diff --name-only --cached | grep '\.py$' || true)

if [ -z "$modified_files" ]; then
    print_message "33" "no modified Python files found."
    exit 0
fi

# format the modified files using ruff
print_message "32" "formatting the following files:"
echo "$modified_files"

# format files
ruff format --line-length 88 $modified_files || true

print_message "32" "formatting complete!"
