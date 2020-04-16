from docker import DockerClient

import config

docker_client = DockerClient(base_url=config.docker_base_url)
docker_client.ping()