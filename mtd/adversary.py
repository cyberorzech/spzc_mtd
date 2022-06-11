import nmap

from loguru import logger

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

PORTS_RANGE = [80, 10000]

def main():
    scan_result = perform_scan()
    open_ports = get_open_ports(scan_result)
    print(open_ports)

if __name__ == "__main__":
    main()