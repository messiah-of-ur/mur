import os
import logging
import subprocess
from pathlib import Path

from job.lifecycle import Lifecycle, FEASIBLE_CONTAINER_ID_LENGTH
from job.murker import MurkerLifecycle


JOB_NAME='murabi'

DOCKER_IMAGE="angler98/murabi:latest"

HOST='host.docker.internal'
ADDRESS_SPLITTER=","


class MurabiLifecycle(Lifecycle):
    def __init__(self, murker_lifecycle: MurkerLifecycle, port: int):
        self._murker_lifecycle = murker_lifecycle
        self._port = port
    
    def run(self) -> None:
        logging.info('Startint murabi on port {}...'.format(self._port))

        proc_store = self._proc_store()
        murabi_env = os.environ.copy()

        cmd = [
            'docker', 'run', 
            '-e', 'MURKER_ADDRESSES', 
            '-e', 'DB_HOST', 
            '-e', 'DB_PORT', 
            '-e', 'DB_USER',
            '-e', 'DB_PASS',
            '-e', 'DB_NAME',
            '-d', '--rm', '-p', '{}:8080'.format(self._port),
            DOCKER_IMAGE,
        ]

        with open(proc_store, 'w') as f:
            p = subprocess.Popen(cmd, env=murabi_env, stdout=f)
            p.wait()
        
        logging.info('Done')
    
    def kill(self) -> None:
        logging.info('Destroying murabi instance...')

        self._kill_docker_container()

        logging.info('Done.')

    def _name(self) -> Path:
        return JOB_NAME

    def _murker_addresses(self) -> str:
        ports = self._murker_lifecycle.active_ports()
        addresses = []

        for port in ports:
            address = "{}:{}".format(HOST, port)
            addresses.insert(address)
        
        return ADDRESS_SPLITTER.join(addresses)
    
    def _log_file(self) -> Path:
        log_dir = self._log_dir()

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        return Path(log_dir, "log")
