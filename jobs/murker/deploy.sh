#!/usr/bin/env bash

set -euo pipefail

MURKER_DIR="${SRC_DIR}/murker"
MURKER_SUBPATH="cmd/murker/murker.go"
MURKER_BINARY="murker.out"
JOB_DIR="${JOBS_DIR}/murker"

source "${LIB_DIR}/common.sh"

MURKER_COUNT="${1}"
STARTER_PORT="${2}"

compileMurker() {
    echo "Compiling muker codebase..."

    pushd "${MURKER_DIR}" &> /dev/null
    go get ./...
    CGO_ENABLED=0 GOOS="$(os)" go build -a -installsuffix cgo -o murker.out "${MURKER_SUBPATH}"
    popd &> /dev/null

    echo "Murker compiled"
}

startMurkers() {
    local pids log_dir log_file

    pids=()

    echo "Starting murkers..."

    log_dir="${JOB_DIR}/log"
    mkdir -p "${log_dir}"

    pushd "${MURKER_DIR}" &> /dev/null
    for ((i = 0; i < "${MURKER_COUNT}"; i++)); do
        MURKER_PORT=$((STARTER_PORT+i))
        echo -en "Starting murker on port ${YELLOW}${MURKER_PORT}${NO_COLOR}..."

        log_file="${log_dir}/${MURKER_PORT}"
        rm -f "${log_file}" && touch "${log_file}"

        MURKER_PORT="${MURKER_PORT}" "./${MURKER_BINARY}" > "${log_file}" &
        pids+=("${!}")
        echo -en "${GREEN}Done${NO_COLOR}.\n"
    done
    popd &> /dev/null

    pushd "${JOB_DIR}" &> /dev/null
    for pid in "${pids[@]}"; do
        echo "${pid}" >> .proc
    done
    popd &> /dev/null

    echo "All murkers started."
}

compileMurker
startMurkers
