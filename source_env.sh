#!/usr/bin/env bash

# Get the directory where this script is located
DOMAIN_FIT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Export variables
export DOMAIN_FIT

# Add script directory to PATH if needed
export PATH="$DOMAIN_FIT:$PATH"
