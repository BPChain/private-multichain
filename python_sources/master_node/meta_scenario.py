"""I offer a function that is run in a Thread to orchestrate the nodes"""

from queue import Queue
from time import sleep
from typing import Tuple

from .scenario_orchestrator import ScenarioOrchestrator
from ..project_logger import set_up_logging

SLAVES_SYNC = Queue()
SETTINGS_SYNC = Queue()

LOG = set_up_logging(__name__)

def run_scylla():
    current_slaves = []
    orchestrator = ScenarioOrchestrator()
    sleep(5)  # wait for things to settle
    orchestrator.issue_assets('meta', 10, 1, True)
    sleep(5)
    LOG.info('Everything is set up')


def run_scenario():
    """I am run in a Thread, and coordinate the scenario"""
    current_slaves = []
    wait_period, transaction_size = 10, 10
    orchestrator = ScenarioOrchestrator()
    sleep(5)  # wait for things to settle
    orchestrator.issue_assets('meta', 10, 1, True)
    sleep(5)
    LOG.info('Everything is set up')
    while True:
        try:
            LOG.info(".....current slaves %s", current_slaves)
            current_slaves = prepare_new_slaves_if_available(current_slaves, orchestrator)
            wait_period, transaction_size = update_if_available(wait_period, transaction_size)
            sleep(wait_period)
            current_slaves = transact_and_update(current_slaves, transaction_size, orchestrator)
        # pylint: disable=broad-except
        except Exception as exception:
            LOG.error("---!!! Unexpected exception occurred %s", exception)


def transact_and_update(current_slaves, size_in_bytes, orchestrator):
    unreachable_slaves = orchestrator.multiple_meta_transactions(current_slaves, size_in_bytes)
    current_slaves = set(current_slaves) - set(unreachable_slaves)
    return current_slaves


def update_if_available(wait_period, byte_size) -> Tuple[int, int]:
    if not SETTINGS_SYNC.empty():
        new_settings = SETTINGS_SYNC.get()
        return new_settings['period'], new_settings['payloadSize']
    return wait_period, byte_size


def prepare_new_slaves_if_available(current_slaves, orchestrator):
    if not SLAVES_SYNC.empty():
        old_slaves = current_slaves
        while not SLAVES_SYNC.empty():
            current_slaves = SLAVES_SYNC.get()
        new_slaves = set(current_slaves) - set(old_slaves)
        if new_slaves:
            LOG.info("--------new slaves %s", new_slaves)
            orchestrator.prepare_slaves(new_slaves)
    return current_slaves
