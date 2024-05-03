import logging
import time


class LogManager:
    """docstring for LogManager."""

    _logger = None

    def __init__(
        self,
        log_name: str,
        log_filepath: str,
        logging_level: int = logging.DEBUG,
        print_on_console: bool = False,
        enable_default_log: bool = False,
    ) -> None:
        self.set_default_log(enabled=enable_default_log)

        logging.basicConfig(level=logging.DEBUG)

        # create logger
        self._logger = logging.getLogger(log_name)

        # log in file
        file_handler = logging.FileHandler(log_filepath, mode="a")
        formatter = logging.Formatter(
            "%(asctime)s-%(message)s", datefmt="%Y%m%d-%H:%M:%S%z"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging_level)
        self._logger.addHandler(file_handler)

        # logging.basicConfig(filename=log_filepath,
        #                     format='%(asctime)s-%(message)s',
        #                     datefmt='%Y%m%d-%H:%M:%S%z',
        #                     level=logging_level)

        if print_on_console:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s-%(message)s", datefmt="%Y%m%d-%H:%M:%S%z"
            )
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging_level)
            self._logger.addHandler(console_handler)

    def set_default_log(self, enabled: bool) -> None:
        log = logging.getLogger("werkzeug")
        # log.setLevel(logging.ERROR)
        # app.logger.disabled = not enabled
        log.disabled = not enabled

        log = logging.getLogger("requests")
        # log.setLevel(logging.ERROR)
        # app.logger.disabled = not enabled
        log.disabled = not enabled

        log = logging.getLogger("urllib3")
        log.setLevel(logging.ERROR)
        # app.logger.disabled = not enabled
        log.disabled = not enabled

    def debug(self, msg: str) -> None:
        self._logger.debug(f"DEBUG - {msg}")

    def info(self, msg: str) -> None:
        self._logger.info(f"INFO - {msg}")

    def warning(self, msg: str) -> None:
        self._logger.warning(f"WARNING - {msg}")

    def error(self, msg: str) -> None:
        self._logger.error(f"ERROR - {msg}")

    def critical(self, msg: str) -> None:
        self._logger.critical(f"CRITICAL - {msg}")


# def unittest():
#     log_manager = LogManager("log_test", "log_test.log")

#     log_manager.debug("this is debug message")
#     log_manager.info("this is info message")
#     log_manager.warning("this is warning message")
#     log_manager.error("this is error message")
#     log_manager.critical("this is critical message")


# if __name__ == "__main__":
#     unittest()

logger = LogManager("log_test", "log_test.log")
