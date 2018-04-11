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
    current_settings = {'frequency': 10, 'payloadSize': 10}
    orchestrator = ScenarioOrchestrator()
    orchestrator.issue_assets('meta', 1, 1, True)
    while True:
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
        sleep(current_settings['frequency'])
        unreachable_slaves = orchestrator.unsafe_multiple_meta_transactions(current_slaves,
                                                                    current_settings['payloadSize'])
        current_slaves = set(current_slaves) - set(unreachable_slaves)
