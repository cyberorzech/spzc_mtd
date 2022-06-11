from sys import exit, stdout, stderr
from loguru import logger
from datetime import date


def main():
    logger.success("Git")

def initialize_logger():
    try:
        log_filename = "logs.log"
        if log_filename == "auto":
            today = date.today()
            log_filename = f"logs/{today.year}-{today.month}-{today.day}.log"
        logger.remove()
        logger.add(stdout, level="INFO")
        logger.add(
            log_filename,
            level="INFO",
            colorize=True,
            retention="5d",
        )
    except KeyError as key_err:
        logger.remove()
        logger.add(stderr)
        logger.critical(f"Key missing in settings file: {str(key_err)}")
        exit(1)
    except Exception as e:
        print(str(e))
        exit(1)
    finally:
        logger.debug("Logger has been initialized")


if __name__ == "__main__":
    initialize_logger()
    main()