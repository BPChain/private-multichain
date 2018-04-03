"""I Run a scenario with the help of the Scenario Orchestrator"""
import sys
import time
from threading import Thread

import python_sources.master_node.master_service as m
from .scenario_orchestrator import ScenarioOrchestrator
from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)


def run_scenario():
    """EVAPCoin Scenario"""
    number_of_slaves = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    orchestrator = ScenarioOrchestrator()
    orchestrator.grant_rights(5, ['receive', 'send'], 'Students')
    orchestrator.grant_rights(5, ['receive'], 'Stores')
    orchestrator.issue_assets("EVAPCoin", 100, 1, True)
    orchestrator.issue_more('EVAPCoin', 20)
    orchestrator.send_assets_to_group(orchestrator.chain_rpc, 'Students', 'EVAPCoin', 3)
    print(orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][3], 'EVAPCoin'))
    orchestrator.send_assets(orchestrator.groups['Students'][3],
                             orchestrator.
                             groups['Stores'][2], 'EVAPCoin', 3)
    orchestrator.send_assets(orchestrator.groups['Students'][4],
                             orchestrator.groups['Stores'][0], 'EVAPCoin', 3)
    print(orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][3], 'EVAPCoin'))
    while True:
        if orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][0], 'EVAPCoin') >= 2:
            orchestrator.send_assets(orchestrator.groups['Students'][0],
                                     orchestrator.groups['Stores'][1], 'EVAPCoin', 2)
        if orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][1], 'EVAPCoin') >= 2:
            orchestrator.send_assets(orchestrator.groups['Students'][1],
                                     orchestrator.groups['Stores'][0], 'EVAPCoin', 2)


def func2():
    LOG.info("####")
    LOG.info(m.chainnodes)


def start_server():
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(m.MasterService, port=60000)
    print("start master")
    server.start()

if __name__ == '__main__':
    Thread(target=start_server).start()
    while True:
        Thread(target=func2).start()
        time.sleep(10)

