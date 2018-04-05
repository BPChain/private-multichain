"""I Run a scenario with the help of the Scenario Orchestrator"""

import time
from http.server import HTTPServer
from threading import Thread

from .http_server import SimpleHTTPRequestHandler, slave_nodes
from .scenario_orchestrator import ScenarioOrchestrator
from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)


def check_chainnodes(orchestrator):
    chainnodes = set(slave_nodes)
    students = set(orchestrator.groups['Students'])
    has_joined(list(chainnodes-students), orchestrator)
    students = set(orchestrator.groups['Students'])
    has_left(list(students-chainnodes), orchestrator)


def has_joined(need_rights, orchestrator):
    for chain_node in need_rights:
        print(chain_node)
        orchestrator.grant_rights(chain_node, ['receive', 'send'], 'Students')


def has_left(has_left, orchestrator):
    for chain_node in has_left:
        orchestrator.revoke_rights(chain_node, ['receive', 'send'])
        orchestrator.groups['Students'].remove(chain_node)


def transfer_assets(orchestrator):
    for student in orchestrator.groups['Students']:
            orchestrator.send_assets(orchestrator.chain_rpc, student, 'EVAPCoin', 1)
            orchestrator.send_assets(student, orchestrator.chain_rpc, 'EVAPCoin', 1)


def run_scenario(iteration_time):
    """EVAPCoin Scenario"""
    orchestrator = ScenarioOrchestrator()
    orchestrator.groups['Students']= []
    while True:
        orchestrator.issue_assets('EVAPCoin', 100, 1, True)
        check_chainnodes(orchestrator)
        time.sleep(iteration_time)
        transfer_assets(orchestrator)


def start_server():
    LOG.info("Masternode is ready for connections")
    httpd = HTTPServer(('masternode', 60000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    Thread(target=start_server).start()
    Thread(target=run_scenario(10)).start()

