"""I offer a function that is run in a Thread to orchestrate the nodes"""
import codecs
import threading
from binascii import b2a_hex
from os import urandom
from queue import Queue
from threading import Thread
from time import sleep

from .scenario_orchestrator import ScenarioOrchestrator
from ..project_logger import set_up_logging

# pylint: disable=broad-except

SLAVES_SYNC = Queue()
SETTINGS_SYNC = Queue()
TERMINATE = False

LOG = set_up_logging(__name__)


def update_settings_blocking():
    LOG.info('Waiting for new settings')
    settings = SETTINGS_SYNC.get()
    sleep(5)  # wait in case there are multiple updates
    while not SETTINGS_SYNC.empty():
        settings = SETTINGS_SYNC.get()
    return settings['nodes'], settings['repetitions']


def run_transactions(slave, config, repetitions):
    LOG.info('Started transactions in Thread %s id: %d', config['name'], threading.get_ident())
    transactions = config['transactions']
    while repetitions > 0:
        repetitions -= 1
        for transaction in transactions:
            if TERMINATE:
                LOG.info('terminating thread %s %d', config['name'], threading.get_ident())
                return
            sleep(transaction['delta'])
            size_bytes = transaction['size']
            quantity = transaction['quantity']
            for _ in range(quantity):
                try:
                    filler_data = codecs.decode(b2a_hex(urandom(size_bytes)))
                    slave.sendwithmetadata(slave.getaddresses()[0], {'meta': 1}, filler_data)
                except Exception as error:
                    LOG.warning(error)
                LOG.info('Completed transaction in Thread %s %d with delta %d', config['name'],
                         threading.get_ident(), transaction['delta'])
        LOG.info('Finished one repetition %s left in %s', config['name'], repetitions)
    LOG.info('Finished repetitions in %s %d', config['name'], threading.get_ident())


def run_scylla():
    current_slaves, orchestrator, settings = set_up()
    slave_threads = []
    while True:
        try:
            LOG.info(".....current slaves %s", current_slaves)
            current_slaves = update_current_slaves(current_slaves, orchestrator)
            global TERMINATE
            configs, repetitions = update_settings_blocking()
            LOG.info(configs)
            while len(current_slaves) != len(configs):
                LOG.warning('Config and slaves are unequal, updating...')
                current_slaves = update_current_slaves(current_slaves, orchestrator)
                sleep(5)
            slave_threads = terminate_threads_blocking(slave_threads)
            for slave, config in zip(current_slaves, configs):
                thread = Thread(target=run_transactions, args=[slave, config, repetitions])
                thread.start()
                slave_threads.append(thread)

        except Exception as exception:
            LOG.error("---!!! Unexpected exception occurred %s", exception)


def terminate_threads_blocking(threads: [Thread]) -> [Thread]:
    global TERMINATE
    TERMINATE = True
    while any(thread.is_alive() for thread in threads):
        sleep(2)
    TERMINATE = False
    return []


def set_up():
    current_slaves = []
    orchestrator = ScenarioOrchestrator()
    sleep(5)  # wait for things to settle
    orchestrator.issue_assets('meta', 10, 1, True)
    sleep(5)
    LOG.info('Everything is set up')
    settings = {'repetitions': 0, 'nodes': []}
    return current_slaves, orchestrator, settings


def update_current_slaves(current_slaves, orchestrator):
    current_slaves = [slave for slave in current_slaves if is_reachable(slave)]
    LOG.debug(current_slaves)
    if not SLAVES_SYNC.empty():
        old_slaves = current_slaves
        while not SLAVES_SYNC.empty():
            current_slaves = SLAVES_SYNC.get()
        new_slaves = set(current_slaves) - set(old_slaves)
        if new_slaves:
            LOG.info("--------new slaves %s", new_slaves)
            orchestrator.prepare_slaves(new_slaves)
    return current_slaves


def is_reachable(slave) -> bool:
    try:
        slave.getinfo()
        return True
        # pylint: disable=broad-except
    except Exception as error:
        LOG.warning('cannot reach %s. Error: %s Removing...', slave, error)
        return False
