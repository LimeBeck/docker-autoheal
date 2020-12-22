from time import sleep
from datetime import datetime, timezone
from docker import DockerClient

import dateutil.parser as parser
from docker.models.containers import Container
from requests.adapters import ReadTimeout

from execute_cmd import execute_cmd
from send_mail import notify_failure
from utils import log, LogLevel
import config

# Test docker connection
test_dc = DockerClient(base_url=config.docker_base_url)
test_dc.ping()
test_dc.close()


def restart_container(container: Container):
    log(f"<27db178e> ({container.name}) Restaring container with timeout {config.container_stop_timeout}")
    container.restart(timeout=config.container_stop_timeout)


def process_container(container: Container):
    log(f"<193643d5> ({container.name}) Container seems to be unhealthy")
    now = datetime.now(timezone.utc)
    failure_time = container.attrs["State"]["Health"]["Log"][-1]["End"]
    try:
        parsed_time = parser.isoparse(failure_time)
        if (now - parsed_time).seconds > config.container_debounce_time:
            execute_cmd(container)
            restart_container(container)
            notify_failure(container)
    except Exception as e:
        log(f"<22105c76> Error in container ({container.name}) processing: {e}", LogLevel.ERROR)


def start():
    sleep(config.container_start_period)
    while True:
        try:
            dc = DockerClient(
                base_url=config.docker_base_url,
                timeout=config.docker_timeout
            )
            for container in dc.containers.list(
                    filters={"health": "unhealthy", "label": [f"{config.container_label}=true"]}):
                process_container(container)
            sleep(config.container_interval)
        except ReadTimeout as e:
            log(f"<7ba9d80d> Connection timed out. Restart containers processing", LogLevel.ERROR)
        except Exception as e:
            log(f"<4be316f> Error: {e}", LogLevel.ERROR)
        finally:
            dc.close()


if __name__ == "__main__":
    start()
