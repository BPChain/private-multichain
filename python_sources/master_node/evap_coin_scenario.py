"""
DEPRECATED
DEPRECATED
DEPRECATED
I Run a scenario with the help of the Scenario Orchestrator"""

from http.server import HTTPServer
from threading import Thread
from time import sleep

from .http_server import SimpleHTTPRequestHandler, SLAVE_NODES
from .scenario_orchestrator import ScenarioOrchestrator
from ..project_logger import set_up_logging


LOG = set_up_logging(__name__)


def check_slave_nodes(orchestrator):
    students = set(orchestrator.groups['Students'])
    has_joined(list(set(SLAVE_NODES) - students), orchestrator)


def has_joined(need_rights, orchestrator):
    for chain_node in need_rights:
        try:
            orchestrator.grant_rights(chain_node, ['receive', 'send'], 'Students')
        except Exception as error:
            has_left(chain_node, orchestrator)
            LOG.critical(error)


def has_left(left_node, orchestrator):
    orchestrator.groups['Students'].remove(left_node)
    SLAVE_NODES.remove(left_node)


def transfer_assets(orchestrator):
    for student in orchestrator.groups['Students']:
        try:
            orchestrator.send_assets(orchestrator.chain_rpc, student, 'EVAPCoin', 1)
            orchestrator.send_assets(student, orchestrator.chain_rpc, 'EVAPCoin', 1)
        # pylint: disable=broad-except
        except Exception as error:
            has_left(student, orchestrator)
            LOG.critical(error)


def run_scenario(iteration_time):
    """EVAPCoin Scenario"""
    sleep(5)
    orchestrator = ScenarioOrchestrator()
    orchestrator.groups['Students'] = []
    orchestrator.issue_assets('EVAPCoin', 200, 1, True)
    while True:
        orchestrator.issue_more('EVAPCoin', 50)
        check_slave_nodes(orchestrator)
        sleep(iteration_time)
        transfer_assets(orchestrator)


def start_server():
    LOG.info("Masternode is ready for connections")
    httpd = HTTPServer(('masternode', 60000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    Thread(target=start_server).start()
    Thread(target=run_scenario(10)).start()
