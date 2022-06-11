import docker
from loguru import logger

@logger.catch
def create(image_name: str, exposed_port: int):
    client = docker.from_env()
    container_id = client.containers.run(
        image_name, detach=True, auto_remove=True, ports={"80/tcp": exposed_port}
    )
    return container_id

@logger.catch
def delete(container_id):
    client = docker.from_env()
    x = client.containers.kill()

if __name__ == "__main__":
    raise NotImplementedError("Use as package")