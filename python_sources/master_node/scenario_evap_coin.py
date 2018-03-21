"""I Run a scenario with the help of the Scenario Orchestrator"""
from time import sleep
import sys

from .scenario_orchestrator import ScenarioOrchestrator

if __name__ == '__main__':
    # Todo: implement waitable Promisses or similar to wait on transaction completion
    NUMBER_OF_SLAVES = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    orchestrator = ScenarioOrchestrator()
    orchestrator.connect_to_slaves(NUMBER_OF_SLAVES)
    orchestrator.grant_rights(5, ['receive', 'send'], 'Students')
    orchestrator.grant_rights(5, ['receive'], 'Stores')
    orchestrator.issue_assets("EVAPCoin", 100, 1, True)
    orchestrator.issue_more('EVAPCoin', 20)
    sleep(10)
    orchestrator.send_assets_to_group(orchestrator.chain_rpc, 'Students', 'EVAPCoin', 3)
    sleep(10)
    print(orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][3], 'EVAPCoin'))
    orchestrator.send_assets(orchestrator.groups['Students'][3],
                             orchestrator.groups['Stores'][2], 'EVAPCoin', 5)
    orchestrator.send_assets(orchestrator.groups['Students'][4],
                             orchestrator.groups['Stores'][0], 'EVAPCoin', 3)
    sleep(10)
    print(orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][3], 'EVAPCoin'))
    while True:
        sleep(10)
        if orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][0], 'EVAPCoin') >= 2:
            orchestrator.send_assets(orchestrator.groups['Students'][0],
                                     orchestrator.groups['Stores'][1], 'EVAPCoin', 2)
        sleep(10)
        if orchestrator.get_quantity_of_asset(orchestrator.groups['Students'][1], 'EVAPCoin') >= 2:
            orchestrator.send_assets(orchestrator.groups['Students'][1],
                                     orchestrator.groups['Stores'][0], 'EVAPCoin', 2)
