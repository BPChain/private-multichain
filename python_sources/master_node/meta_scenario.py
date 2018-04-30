"""I offer a function that is run in a Thread to orchestrate the nodes"""
import codecs
import threading
from binascii import b2a_hex
from os import urandom
from queue import Queue
from time import sleep
from threading import Thread

from .scenario_orchestrator import ScenarioOrchestrator
from ..project_logger import set_up_logging

# pylint: disable=broad-except

SLAVES_SYNC = Queue()
SETTINGS_SYNC = Queue()
TERMINATE = False

LOG = set_up_logging(__name__)


def update_settings_blocking():
    settings = SETTINGS_SYNC.get()
    sleep(5)  # wait in case there are multiple updates
    while not SETTINGS_SYNC.empty():
        settings = SETTINGS_SYNC.get()
    return settings['nodes'], settings['repetitions']


def run_transactions(slave, config, repetitions):
    LOG.info('Started transactions in Thread %s id: %d', config['name'], threading.get_ident())
    transactions = config['transactions']
    while repetitions >= 0:
        repetitions -= 1
        for transaction in transactions:
            if TERMINATE:
                LOG.info('terminating thread %d', threading.get_ident())
                return
            sleep(transaction['delta'])
            size_bytes = transaction['size']
            try:
                filler_data = codecs.decode(b2a_hex(urandom(size_bytes)))
                answer = slave.sendwithmetadata(slave.getaddresses()[0], {'meta': 1}, filler_data)
                LOG.info("Transaction ID %s", answer)
            except Exception as error:
                LOG.warning(error)
            LOG.info('Completed transactions in Thread %d', threading.get_ident())
    LOG.info('Finished repetitions in %s %d', config['name'], threading.get_ident())


def run_scylla():
    current_slaves, orchestrator, settings = set_up()
    while True:
        try:
            LOG.info(".....current slaves %s", current_slaves)
            current_slaves = update_current_slaves(current_slaves, orchestrator)
            global TERMINATE
            configs, repetitions = update_settings_blocking()
            LOG.info(configs)
            TERMINATE = True
            while len(current_slaves) != len(configs):
                LOG.warning('Config and slaves are unequal')
                current_slaves = update_current_slaves(current_slaves, orchestrator)
            for slave, config in zip(current_slaves, configs):
                TERMINATE = False
                Thread(target=run_transactions, args=[slave, config, repetitions]).start()
        except Exception as exception:
            LOG.error("---!!! Unexpected exception occurred %s", exception)


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
    if not SLAVES_SYNC.empty():
        old_slaves = current_slaves
        while not SLAVES_SYNC.empty():
            current_slaves = SLAVES_SYNC.get()
        new_slaves = set(current_slaves) - set(old_slaves)
        if new_slaves:
            LOG.info("--------new slaves %s", new_slaves)
            orchestrator.prepare_slaves(new_slaves)
    return current_slaves
