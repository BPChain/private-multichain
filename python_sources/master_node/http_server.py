"""I receive multichain username, password and ip from slave nodes and get their Savoir instances
to control them """

import json
from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
from Savoir import Savoir
from .meta_scenario import SLAVES_SYNC

from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)
SLAVE_NODES = []


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
        global SLAVE_NODES
        user = credentials['user']
        password = credentials['password']
        host = credentials['host']
        rpc_port = credentials['rpc_port']
        chain_node = Savoir(user, password, host, rpc_port, "bpchain")
        SLAVE_NODES = SLAVE_NODES + [chain_node]
        LOG.info("Added connection to slave %d", len(SLAVE_NODES))
        LOG.info(SLAVE_NODES)
        SLAVES_SYNC.put([slave for slave in SLAVE_NODES])



def start_slave_server():
    LOG.info("Masternode is ready for connections")
    httpd = HTTPServer(('masternode', 60000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
