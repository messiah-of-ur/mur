import os
import subprocess
from enum import Enum
from typing import List
from pathlib import Path
from abc import ABCMeta, abstractmethod


FEASIBLE_CONTAINER_ID_LENGTH=10


class Environment(Enum):
    CODE_DIR = 'CODE_DIR'
    JOB_DIR = 'JOB_DIR'


class Lifecycle:
    __metaclass__ = ABCMeta

    @abstractmethod
    def fetch_dependencies(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def compile(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def kill(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _gen_dir(self) -> Path:
        jobs_dir = os.getenv(Environment.JOB_DIR.value)
        gen_dir = Path(jobs_dir, 'gen')
        job_name = self._name()

        gen_dir = Path(gen_dir, job_name)

        if not os.path.exists(gen_dir):
            os.mkdir(gen_dir)

        return gen_dir

    def _bin_dir(self) -> Path:
        gen_dir = self._gen_dir()
        return Path(gen_dir, 'bin')
    
    def _log_dir(self) -> Path:
        gen_dir = self._gen_dir()
        return Path(gen_dir, 'log')

    def _proc_store(self) -> Path:
        gen_dir = self._gen_dir()
        return Path(gen_dir, 'proc_store')

    @staticmethod
    def _run_process_from_dir(dir: Path, cmd: List[str]) -> None:
        cwd = os.getcwd()

        try:
            os.chdir(dir)
            subprocess.run(cmd)
        finally:
            os.chdir(cwd)

    def _kill_docker_container(self) -> None:
        proc_store = self._proc_store()

        with open(proc_store, 'r') as f:
            container_id = f.readline()[:FEASIBLE_CONTAINER_ID_LENGTH]

            p = subprocess.Popen(['docker', 'kill', container_id])
            p.wait()
        
        open(proc_store, 'w').close()
