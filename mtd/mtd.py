from time import sleep
from loguru import logger


from src.logger import initialize_logger
from src.container import *

IMAGE_NAME = "webserver"
SLEEP_INTERVAL = 10 #[s]

def main():
    container_id = create(image_name=IMAGE_NAME, exposed_port=80)
    logger.success(f"Docker started {container_id}")
    sleep(SLEEP_INTERVAL)
    delete(container_id)
    logger.success(f"Deleted container {container_id}")

if __name__ == "__main__":
    initialize_logger()
    main()
