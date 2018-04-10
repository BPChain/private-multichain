"""I offer a function that is run in a Thread to orchestrate the nodes"""

from queue import LifoQueue
from threading import Lock
from time import sleep

from ..project_logger import set_up_logging

SCENARIO_LOCK = Lock()
SLAVES_SYNC = LifoQueue()
SETTINGS_SYNC = LifoQueue()

LOG = set_up_logging(__name__)


def run_scenario():
    current_slaves = []
    current_settings = {'frequency': 10, 'payloadSize': 0}
    while True:
        if not SLAVES_SYNC.empty():
            current_slaves = SLAVES_SYNC.get()
        if not SETTINGS_SYNC.empty():
            current_settings = SETTINGS_SYNC.get()
        LOG.info("settings %s slaves %s", current_settings, current_slaves)
        sleep(current_settings['frequency'])
        for slave in current_slaves:
            LOG.info("in loop")
            LOG.info("settings %s slaves %s", current_settings, current_slaves)
            # slave.sendAsset(CURRENT_SETTINGS['size'])
