"""I offer a function that is run in a Thread to orchestrate the nodes"""
import codecs
import threading
from threading import Thread

from binascii import b2a_hex
from os import urandom
from queue import Queue
from time import sleep

from ..project_logger import set_up_logging

# pylint: disable=broad-except
# pylint: disable=global-statement

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


def run_scenario():
    current_slaves = []
    current_scenario = Scenario()
    while True:
        try:
            LOG.info(".....current slaves %s", current_slaves)
            current_slaves = update_current_slaves(current_slaves)
            global TERMINATE
            configs, repetitions = update_settings_blocking()
            LOG.info(configs)
            while len(current_slaves) != len(configs):
                LOG.warning('Config and slaves are unequal, udating...')
                current_slaves = update_current_slaves(current_slaves)
                sleep(5)
            current_scenario.stop()
            current_scenario = Scenario().start(current_slaves, configs, repetitions)

        except Exception as exception:
            LOG.error("---!!! Unexpected exception occurred %s", exception)


def update_current_slaves(current_slaves):
    current_slaves = [slave for slave in current_slaves if slave.is_alive()]
    LOG.debug(current_slaves)
    if not SLAVES_SYNC.empty():
        while not SLAVES_SYNC.empty():
            current_slaves = SLAVES_SYNC.get()
    return current_slaves



class Scenario:
    def __init__(self):
        self.is_running = False

    def __run_transactions(self, slave, config, repetitions):
        """Publish desired amount of data defined in config to root stream"""
        LOG.info('Started transactions in Thread %s id: %d', config['name'], threading.get_ident())
        transactions = config['transactions']
        while repetitions > 0:
            repetitions -= 1
            for transaction in transactions:
                sleep(transaction['delta'])
                if not self.is_running:
                    LOG.info('terminating thread %s %d', config['name'], threading.get_ident())
                    return
                size_bytes = transaction['size']
                quantity = transaction['quantity']
                for _ in range(quantity):
                    try:
                        filler_data = codecs.decode(b2a_hex(urandom(size_bytes)))
                        slave.transact(config['name'], filler_data)
                    except Exception as error:
                        LOG.warning(error)
                    LOG.info('Completed transaction in Thread %s %d with delta %d', config['name'],
                             threading.get_ident(), transaction['delta'])
            LOG.info('Finished one repetition %s left in %s', config['name'], repetitions)
        LOG.info('Finished repetitions in %s %d', config['name'], threading.get_ident())

    def start(self, current_slaves, configs, repetitions):
        self.is_running = True
        for slave, config in zip(current_slaves, configs):
            thread = Thread(target=self.__run_transactions, args=[slave, config, repetitions])
            thread.start()
        return self

    def stop(self):
        self.is_running = False
