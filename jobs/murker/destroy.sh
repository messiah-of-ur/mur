#!/usr/bin/env bash

set -euo pipefail

JOB_DIR="${JOBS_DIR}/murker"
PROC_FILE="${JOB_DIR}/.proc"

source "${LIB_DIR}/common.sh"

killMurkers() {
    while read -r pid; do
        echo -en "Deleting murker with pid ${YELLOW}${pid}${NO_COLOR}..."

        if ! kill "${pid}" > /dev/null 2>&1; then
            echo -en "\n${RED}ERROR:${NO_COLOR} There was no murker running on pid ${YELLOW}${pid}${NO_COLOR}."
        fi

        echo -en "${GREEN}Done${NO_COLOR}.\n"

    done < "${PROC_FILE}"

    true > "${PROC_FILE}"
}

killMurkers
