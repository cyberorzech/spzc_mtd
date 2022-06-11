from python_on_whales import docker
from loguru import logger
from json import dump
from datetime import datetime


@logger.catch
def create(image_name: str, exposed_port: int):
    container_id = docker.run(
        image_name, detach=True, publish=[(exposed_port, 80)], remove=True
    )
    return container_id


@logger.catch
def delete_container(container_id):
    docker.stop(container_id)


@logger.catch
def delete_active_containers():
    active_containers = docker.ps()
    docker.stop(*active_containers)


@logger.catch
def export_container_info(container, exposed_port, path="./exposed_container.json"):
    container_info = {
        "id": container.id,
        "exposed_port": exposed_port,
        "timestamp": datetime.timestamp(datetime.now()),
    }
    with open(path, "w") as f:
        dump(container_info, f)


if __name__ == "__main__":
    raise NotImplementedError("Use as package")
