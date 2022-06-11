from time import sleep
from loguru import logger
from random import randint


from src.logger import initialize_logger
from src.container import *

IMAGE_NAME = "webserver"
SLEEP_INTERVAL = 10 #[s]

def main():
    while(True):
        exposed_port = 123
        container_id = create(image_name=IMAGE_NAME, exposed_port=exposed_port)
        logger.success(f"Container exposed on port {exposed_port} with id {container_id}")
        sleep(SLEEP_INTERVAL)
        delete(container_id)
        logger.success(f"Deleted container {container_id}")

if __name__ == "__main__":
    initialize_logger()
    main()
