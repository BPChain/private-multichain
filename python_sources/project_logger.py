"""I set up a logger for a module."""
import logging
from logging import Logger


def set_up_logging(name) -> Logger:
    new_logger = logging.getLogger(name)
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s || In: %(module)s at: '
                                  '%(lineno)d', datefmt='%I:%M:%S')
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    new_logger.setLevel(logging.INFO)
    new_logger.addHandler(console)
    return new_logger
