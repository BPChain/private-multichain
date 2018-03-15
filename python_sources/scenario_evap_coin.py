from .master_node.scenario_orchestrator import ScenarioOrchestrator
from time import sleep
import sys

if __name__ == '__main__':
    number_of_slaves = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    orchestrator = ScenarioOrchestrator()
    orchestrator.connect_to_slaves(number_of_slaves)
    orchestrator.grant_rights(5, ['receive', 'send'], 'Students')
    orchestrator.grant_rights(5, ['receive'], 'Stores')
    orchestrator.issue_assets('EVAPCoin', 100, 1)
    orchestrator.send_assets_to_group(orchestrator.chain_rpc, 'Students', 'EVAPCoin', 20)
    orchestrator.revoke_rights('Students', ['receive']) # I don't want students to give tokens to each other muhahaha
    orchestrator.send_assets(orchestrator.groups['Students'][0], orchestrator.groups['Stores'][1], 'EVAPCoin', 2)
    orchestrator.send_assets(orchestrator.groups['Students'][3], orchestrator.groups['Stores'][2], 'EVAPCoin', 5)
    orchestrator.send_assets(orchestrator.groups['Students'][4], orchestrator.groups['Stores'][0], 'EVAPCoin', 3)
    while True:
        sleep(1000000)  # So Docker will not stop container