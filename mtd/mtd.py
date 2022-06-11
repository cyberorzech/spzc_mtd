import signal
import sys
from time import sleep
from loguru import logger
from random import randint

from src.logger import initialize_logger
from src.container import *

IMAGE_NAME = "webserver"
SLEEP_INTERVAL = 6  # [s]
PUBLISHED_PORTS_RANGE = [5000, 6000]
CONFIG_PATH = "./exposed_container.json"
LOG_FILENAME = "mtd_logs.log"

def main():
    while True:
        exposed_port = randint(*PUBLISHED_PORTS_RANGE)
        container = create(image_name=IMAGE_NAME, exposed_port=exposed_port)
        logger.success(f"Container exposed on port {exposed_port} with id {container}")
        export_container_info(container, exposed_port, CONFIG_PATH)
        logger.success(f"Config at {CONFIG_PATH} has been updated")
        sleep(SLEEP_INTERVAL)
        delete_container(container)
        logger.success(f"Deleted container {container}")


def signal_handler(sig, frame):
    logger.info("Cleaning containers...")
    delete_active_containers()
    sys.exit(0)


if __name__ == "__main__":
    initialize_logger(LOG_FILENAME)
    signal.signal(signal.SIGINT, signal_handler)
    main()
