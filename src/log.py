import logging
import sys

__logger_stdout = logging.getLogger("detection_license_plates")

__formatter = logging.Formatter("{%(name)s} - <%(asctime)s> - [%(levelname)-7s] - %(message)s")

__handler_stdout = logging.StreamHandler(sys.stdout)
__handler_stdout.setFormatter(__formatter)
__logger_stdout.addHandler(__handler_stdout)
__logger_stdout.setLevel(logging.INFO)
__logger_stdout.propagate = False


def debug(msg: str):
    if __logger_stdout.isEnabledFor(logging.DEBUG):
        __logger_stdout.debug(msg)


def info(msg: str):
    __logger_stdout.info(msg)


def warn(msg: str):
    __logger_stdout.warning(msg)


def error(msg: str):
    __logger_stdout.error(msg)


def exception(e: Exception):
    __logger_stdout.exception(e)