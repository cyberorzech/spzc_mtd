from python_on_whales import docker
from loguru import logger

@logger.catch
def create(image_name: str, exposed_port: int):
    container_id = docker.run(
        image_name, detach=True, publish=[(exposed_port, 80)], remove=True
    )
    return container_id

@logger.catch
def delete(container_id):
    docker.stop(container_id)
    
if __name__ == "__main__":
    raise NotImplementedError("Use as package")