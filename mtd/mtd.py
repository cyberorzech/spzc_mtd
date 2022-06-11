import signal
import sys
from time import sleep
from loguru import logger
from random import randint


from src.logger import initialize_logger
from src.container import *

IMAGE_NAME = "webserver"
SLEEP_INTERVAL = 5 #[s]
PUBLISHED_PORTS_RANGE = [5000, 6000]

def main():
    while(True):
        exposed_port = randint(*PUBLISHED_PORTS_RANGE)
        container_id = create(image_name=IMAGE_NAME, exposed_port=exposed_port)
        logger.success(f"Container exposed on port {exposed_port} with id {container_id}")
        sleep(SLEEP_INTERVAL)
        delete_container(container_id)
        logger.success(f"Deleted container {container_id}")

def signal_handler(sig, frame):
    logger.info("Cleaning containers...")
    delete_active_containers()
    sys.exit(0)

if __name__ == "__main__":
    initialize_logger()
    signal.signal(signal.SIGINT, signal_handler)
    main()
