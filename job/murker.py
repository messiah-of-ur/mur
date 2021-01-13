import os
import sys
import logging
import subprocess
import signal
import psutil
from typing import List
from pathlib import Path

from job.lifecycle import Lifecycle, Environment


MURKER_EXECUTABLE_PATH='cmd/murker/murker.go'
JOB_NAME='murker'
MURKER_PORT='MURKER_PORT'


class MurkerLifecycle(Lifecycle):
    def __init__(self, ports: List[int]):
        self.ports = ports
    
    def fetch_dependencies(self) -> None:
        logging.info('Fetching murker dependencies...')

        self._run_process_from_murker_dir(cmd=['go', 'get', './...'])

        logging.info('Done.')

    def compile(self) -> None:
        logging.info('Compiling murker...')

        out = self._murker_binary_path()
        self._run_process_from_murker_dir(cmd=['go', 'build', '-o', out, MURKER_EXECUTABLE_PATH])

        logging.info('Done.')

    def run(self) -> None:
        log_dir = self._log_dir()

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        bin = self._murker_binary_path()
        proc_store = self._proc_store()
        port_store = self._port_store()

        for port in self.ports:
            logging.info('Starting murker on port {}...'.format(port))

            murker_env = os.environ.copy()
            murker_env[MURKER_PORT] = str(port)

            murker = None

            log = Path(log_dir, str(port))

            with open(log, 'w') as f:
                murker = subprocess.Popen([bin], env=murker_env, stdout=f, stderr=f)

            with open(proc_store, 'a') as f:
                f.write('{}\n'.format(murker.pid))
            
            with open(port_store, 'a') as f:
                f.write('{}\n'.format(port))

            logging.info('Done.')

    def kill(self) -> None:
        proc_store = self._proc_store()

        with open(proc_store, 'r') as f:
            pids = f.readlines()
            
            for pid in pids:
                logging.info('Killing murker with pid {}...'.format(pid))

                p = psutil.Process(int(pid))
                p.terminate()

                logging.info('Done.')
                
        open(proc_store, 'w').close()

        port_store = self._port_store()
        open(port_store, 'w').close()

    def active_ports(self) -> List[int]:
        port_store = self._port_store()

        ports = []

        with open(port_store, 'r') as f:
            lines = f.readlines()

            for line in lines:
                ports.append(int(line))

        return ports

    def _name(self) -> Path:
        return JOB_NAME

    def _murker_dir(self) -> Path:
        code_dir = os.getenv(Environment.CODE_DIR.value)
        print(code_dir)
        return Path(code_dir, JOB_NAME)

    def _murker_binary_path(self) -> Path:
        bin_dir = self._bin_dir()
        return Path(bin_dir, 'murker.out')
    
    def _proc_store(self) -> Path:
        gen_dir = self._gen_dir()
        return Path(gen_dir, 'proc_store')
    
    def _port_store(self) -> Path:
        gen_dir = self._gen_dir()
        return Path(gen_dir, 'port_store')

    def _run_process_from_murker_dir(self, cmd: List[str]) -> None:
        murker_dir = self._murker_dir()
        self._run_process_from_dir(murker_dir, cmd)
