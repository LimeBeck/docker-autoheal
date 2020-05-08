#!/usr/bin/env python3

from docker import DockerClient

import config

docker_client = DockerClient(base_url=config.docker_base_url)
docker_client.ping()
docker_client.close()

exit(0)
