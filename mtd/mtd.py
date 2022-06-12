import signal
import sys
from time import sleep, perf_counter
from loguru import logger
from random import randint

from src.logger import initialize_logger
from src.container import *

IMAGE_NAME = "webserver"
SLEEP_INTERVAL = 15  # [s]
PUBLISHED_PORTS_RANGE = [10000, 15000]
CONFIG_PATH = "./exposed_container.json"
LOG_FILENAME = "mtd_logs.log"

downtimes = list()

def main():
    downtime_start = 0
    while True:
        exposed_port = randint(*PUBLISHED_PORTS_RANGE)
        container = create(image_name=IMAGE_NAME, exposed_port=exposed_port)
        logger.success(f"Container exposed on port {exposed_port} with id {container}")
        export_container_info(container, exposed_port, CONFIG_PATH)
        logger.success(f"Config at {CONFIG_PATH} has been updated")
        if downtime_start != 0:
            downtime_end = perf_counter()
            downtime = downtime_end - downtime_start
            logger.info(f"Downtime: {downtime}")
            downtime_start = 0
            downtimes.append(downtime)
        sleep(SLEEP_INTERVAL)
        downtime_start = perf_counter()
        delete_container(container)
        logger.success(f"Deleted container {container}")

# TODO
def reconnaissance_detection():
    pass

def signal_handler(sig, frame):
    logger.info("Cleaning containers...")
    delete_active_containers()
    logger.success(f"Mean downtime: {sum(downtimes) / len(downtimes)}")
    sys.exit(0)


if __name__ == "__main__":
    initialize_logger(LOG_FILENAME)
    signal.signal(signal.SIGINT, signal_handler)
    main()
