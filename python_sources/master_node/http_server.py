"""I receive multichain username, password and ip from slave nodes and get their Savoir instances
to control them """

import json
from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
from Savoir import Savoir
from .meta_scenario import SLAVES_SYNC

from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)
_SLAVE_NODES = []


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """I handle requests form the slaves who send their user data"""

    # pylint: disable=invalid-name
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.add_slave_nodes(json.loads(body.decode('utf-8')))

    def add_slave_nodes(self, credentials):
        # pylint: disable=global-statement
        global _SLAVE_NODES
        unreachables = [slave for slave in _SLAVE_NODES if not self.is_reachable(slave)]
        user = credentials['user']
        password = credentials['password']
        host = credentials['host']
        rpc_port = credentials['rpc_port']
        chain_node = Savoir(user, password, host, rpc_port, "bpchain")
        _SLAVE_NODES = [slave for slave in _SLAVE_NODES if slave not in unreachables] + [chain_node]
        LOG.info("Added connection to slave %d", len(_SLAVE_NODES))
        LOG.info(_SLAVE_NODES)
        SLAVES_SYNC.put(_SLAVE_NODES)


    def is_reachable(self, slave: Savoir):
        try:
            slave.getinfo()
            return True
        #pylint: disable=broad-except
        except Exception as error:
            LOG.warning('cannot reach %s. Error: %s Removing...', slave, error)
            return False


def start_slave_server():
    LOG.info("Masternode is ready for connections")
    httpd = HTTPServer(('masternode', 60000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
