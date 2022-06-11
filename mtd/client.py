import requests
from time import sleep, perf_counter
from loguru import logger
from json import load

from src.logger import initialize_logger

SLEEP_INTERVAL = 10
CONFIG_PATH = "./exposed_container.json"
LOG_FILENAME = "client_logs.log"

@logger.catch
def get_containers_port():
    with open(CONFIG_PATH) as f:
        exposed_container_info = load(f)
    return exposed_container_info["exposed_port"]

@logger.catch
def perform_request(port: int):
    try:
        url = f"http://127.0.0.1:{port}"
        web_content = requests.get(url)
        return web_content
    except requests.exceptions.ConnectionError as ce:
        return str(ce)

@logger.catch
def measure_requests():
    success_count = 0
    failure_count = 0

    while(True):
        port = get_containers_port()
        response = perform_request(port)
        if "Response [200]" in str(response):
            success_count += 1
        else:
            failure_count += 1
        logger.success(f"{success_count=}, {failure_count=}")
        # sleep(0.2)

@logger.catch
def measure_downtime():
    downtime = 0
    uptime = 0
    loop_count = 0

    while(True):
        start_time = perf_counter()
        port = get_containers_port()
        response = perform_request(port)
        if "Response [200]" in str(response):
            end_time = perf_counter()
            uptime += end_time - start_time
        else:
            end_time = perf_counter()
            downtime += end_time - start_time
        loop_count += 1
        if loop_count % 1000 == 0:
            logger.success(f"Uptime: {round(uptime, 2)}[s], Downtime: {round(downtime, 2)}[s]")
            loop_count = 0


def main():
    #measure_requests()
    measure_downtime()

if __name__ == "__main__":
    initialize_logger(LOG_FILENAME)
    main()