#!/usr/bin/env bash

set -euo pipefail

RED="\033[1;31m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
NO_COLOR="\033[0m"

os() {
    if uname -a | grep Darwin &> /dev/null; then
        echo "darwin"
    else
        echo "linux"
    fi
}
