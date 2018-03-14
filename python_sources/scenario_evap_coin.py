from ..python_sources.master_node.scenario_orchestrator import ScenarioOrchestrator


if __name__ == '__main__':
    orchestrator = ScenarioOrchestrator()
    orchestrator.connect_to_slaves(10)
    orchestrator.grant_rights(5, ['receive', 'send'], 'Students')
    orchestrator.grant_rights(5, ['receive'], 'Stores')
    orchestrator.issue_assets('EVAPCoin', 100, 1)
    orchestrator.send_assets_to_group(orchestrator.chain_rpc, 'Students', 20)
    orchestrator.revoke_rights('Students', ['receive']) # I don't want students to give tokens to each other muhahaha
    orchestrator.send_assets(orchestrator.groups['Students'][0], orchestrator.groups['Stores'][0], 'EVAPCoin', 2)
    orchestrator.send_assets(orchestrator.groups['Students'][3], orchestrator.groups['Stores'][2], 'EVAPCoin', 5)
    orchestrator.send_assets(orchestrator.groups['Students'][4], orchestrator.groups['Stores'][0], 'EVAPCoin', 3)
