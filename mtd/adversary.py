import nmap
import requests
from time import sleep
from loguru import logger
from tqdm import trange

from src.logger import initialize_logger

@logger.catch
def perform_scan():
    nm = nmap.PortScanner()
    result = nm.scan('127.0.0.1', ports=f"{PORTS_RANGE[0]}-{PORTS_RANGE[1]}")
    return result

@logger.catch
def get_open_ports(nmap_scan_result: dict) -> list:
    OPEN_PORT = "open"
    HTTP_SERVICE = "http"
    result = list()
    scanned_ports = [*nmap_scan_result["scan"]["127.0.0.1"]["tcp"]]
    for port in scanned_ports:
        state = nmap_scan_result["scan"]["127.0.0.1"]["tcp"][port]["state"]
        service_name = nmap_scan_result["scan"]["127.0.0.1"]["tcp"][port]["name"]
        if state == OPEN_PORT and service_name == HTTP_SERVICE:
            result.append(port)
    return result

@logger.catch
def perform_trial_request(port):
    url = f"http://127.0.0.1:{port}"
    response = requests.get(url)
    return response

@logger.catch
def perform_exploit():
    for _ in trange(EXPLOIT_TIME): sleep(EXPLOIT_TIME)

LOG_FILENAME = "adversary_logs.log"
PORTS_RANGE = [80, 100]
EXPLOIT_TIME = 2 #[s]


def main():
    successful_attacks_count = 0
    unsuccessful_attacks_count = 0
    loops_count = 0
    while(True):
        scan_result = perform_scan()
        open_ports = get_open_ports(scan_result)
        logger.info(f"{open_ports=}")
        # assumption: there should be one open http port at a time
        try:
            if len(open_ports) == 0:
                raise RuntimeError("Found no open ports!")
            if len(open_ports) > 1:
                raise RuntimeError(f"Unexpected data. NMap found more than one open http port. {open_ports=}")
            response = perform_trial_request(open_ports[0])
            if not "Response [200]" in str(response):
                raise RuntimeError(f"Invalid http response")

            logger.success(f"So far so good. Performing exploit on port {open_ports[0]}...")
            perform_exploit()
            if not "Response [200]" in str(response):
                raise RuntimeError(f"Attack unsuccessful")

        except RuntimeError as re:
            unsuccessful_attacks_count += 1
            logger.warning(re)
            continue
        
        successful_attacks_count += 1
        logger.success(f"Attack successful")
        loops_count += 1
        if loops_count % 10 == 0:
            logger.info(f"{successful_attacks_count=}, {unsuccessful_attacks_count=}")


if __name__ == "__main__":
    initialize_logger(LOG_FILENAME)
    main()