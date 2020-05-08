from docker.models.containers import Container

from labels import FAILURE_CMD
from utils import log


def execute_cmd(container: Container):
    if FAILURE_CMD not in container.labels.keys():
        return
    cmd: str = container.labels[FAILURE_CMD]
    log(f"<6065059f> ({container.name}) Execute cmd: {cmd}")
    exit_code, output = container.exec_run(cmd=cmd)
    log(
        f"<320e52a6> ({container.name}) Executed failure cmd. Exited with {exit_code} and output: \n {str(output, 'utf-8')}")
