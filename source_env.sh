#!/usr/bin/env bash
# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
# Add script directory and its subdirectory to the PATH
export PATH="$SCRIPT_DIR:$SCRIPT_DIR/AlphaFold:$PATH"