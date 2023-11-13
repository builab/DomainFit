#!/usr/bin/env bash

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"
echo $SCRIPT_DIR

# Add execute permissions to Python scripts in the current directory
for script in *.py; do
    if [ ! -x "$script" ]; then
        chmod +x "$script"
    fi
done

# Add script directory to the PATH
export PATH="$PATH:$SCRIPT_DIR"
