"""I Run a scenario with the help of the Scenario Orchestrator"""
import time
from http.server import HTTPServer
from threading import Thread

import python_sources.master_node.master_service as m
from .scenario_orchestrator import ScenarioOrchestrator, SimpleHTTPRequestHandler, test
from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)


def check_chainnodes(orchestrator):
    orchestrator.groups['Students']= []
    chainnodes = set(test)
    students = set(orchestrator.groups['Students'])
    has_joined(list(chainnodes-students), orchestrator)
    has_left(list(students-chainnodes), orchestrator)

def has_joined(need_rights, orchestrator):
    print('####################')
    print(need_rights)
    for chain_node in need_rights:
        print(chain_node)
        orchestrator.grant_rights(chain_node, ['receive', 'send'], 'Students')

def has_left(has_left, orchestrator):
    for chain_node in has_left:
        orchestrator.revoke_rights(chain_node, ['receive', 'send'])
        orchestrator.groups['Students'].remove(chain_node)

def run_scenario():
    """EVAPCoin Scenario"""
    orchestrator = ScenarioOrchestrator()
    check_chainnodes(orchestrator)



def func2():
    LOG.info("####")
    LOG.info(m.chainnodes)


def start_server():
    httpd = HTTPServer(('masternode', 60000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    Thread(target=start_server).start()
    while True:
        Thread(target=run_scenario).start()
        time.sleep(10)

