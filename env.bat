set BASE_DIR=%cd%
set CODE_DIR=%cd%\code
set JOB_DIR=%cd%\job
set GOPATH=%cd%
set PYTHONPATH=%PYTHONPATH%;%cd%

set DB_HOST=host.docker.internal
set DB_PORT=5432
set DB_USER=murabi
set DB_PASS=murabi
set DB_NAME=murabi

set MURKER_ADDRESSES=host.docker.internal:9000,host.docker.internal:9001

set POSTGRES_PASSWORD=%DB_PASS%
set POSTGRES_USER=%DB_USER%
