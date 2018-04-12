"""I offer a function that is run in a Thread to orchestrate the nodes"""

from queue import Queue
from threading import Lock
from time import sleep

from .scenario_orchestrator import ScenarioOrchestrator
from ..project_logger import set_up_logging

SLAVES_SYNC = Queue()
SETTINGS_SYNC = Queue()

LOG = set_up_logging(__name__)


def run_scenario():
    current_slaves = []
    current_settings = {'period': 10, 'payloadSize': 10}
    orchestrator = ScenarioOrchestrator()
    sleep(5)  # wait for things to settle
    orchestrator.issue_assets('meta', 10, 1, True)
    sleep(5)
    LOG.info('Everything is set up')
    while True:
        try:
            LOG.info(".....current slaves %s", current_slaves)
            if not SLAVES_SYNC.empty():
                old_slaves = current_slaves
                while not SLAVES_SYNC.empty():
                    current_slaves = SLAVES_SYNC.get()
                LOG.info("###### old %s current %s", old_slaves, current_slaves)
                new_slaves = set(current_slaves) - set(old_slaves)
                LOG.info("--------new slaves %s", new_slaves)
                if new_slaves:
                    orchestrator.prepare_slaves(new_slaves)
            if not SETTINGS_SYNC.empty():
                current_settings = SETTINGS_SYNC.get()
            sleep(current_settings['period'])
            unreachable_slaves = orchestrator.unsafe_multiple_meta_transactions(
                current_slaves, current_settings['payloadSize'])
            current_slaves = set(current_slaves) - set(unreachable_slaves)
        # pylint: disable=broad-except
        except Exception as exception:
            LOG.error("---!!! Unexpected exception occurred %s", exception)
