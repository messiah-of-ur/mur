import os
import time
import logging
import subprocess
from pathlib import Path

from job.lifecycle import Lifecycle, Environment, FEASIBLE_CONTAINER_ID_LENGTH


MURDB_PORT=5432
JOB_NAME="db"
PGPASSWORD="PGPASSWORD"
POSTGRES_PASSWORD="POSTGRES_PASSWORD"


class MurDBLifecycle(Lifecycle):
    def __init__(self):
        pass

    def run(self) -> None:
        logging.info('Startint mur db on port {}...'.format(MURDB_PORT))

        proc_store = self._proc_store()

        murdb_env = os.environ.copy()

        cmd = [
            'docker', 'run', '--rm', '--name', 'pq',
            '-e', 'POSTGRES_PASSWORD',
            '-e', 'POSTGRES_USER',
            '-p', '{}:{}'.format(MURDB_PORT, MURDB_PORT), '-d', 'postgres'
        ]

        with open(proc_store, 'w') as f:
            p = subprocess.Popen(cmd, env=murdb_env, stdout=f)
            p.wait()

        time.sleep(7)

        murdb_env[PGPASSWORD] = os.getenv(POSTGRES_PASSWORD)

        schema_path = self._schema_path()
        schema_up_cmd = ['psql', '-h', 'localhost',  '-d', 'murabi', '-U', 'murabi',  '-f', schema_path]

        p = subprocess.Popen(schema_up_cmd, env=murdb_env)
        p.wait()
        
        logging.info('Done')

    def kill(self) -> None:
        logging.info('Destroying mur db instance...')

        self._kill_docker_container()

        logging.info('Done.')

    def _name(self) -> Path:
        return JOB_NAME

    def _schema_path(self) -> Path:
        code_dir = os.getenv(Environment.CODE_DIR.value)
        return Path(code_dir, 'murabi', 'schema', 'up.sql')
