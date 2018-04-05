"""I receive multichain username, password and ip from slave nodes and get their Savoir instances to control them """

import json
from http.server import BaseHTTPRequestHandler

from Savoir import Savoir

from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)

SLAVE_NODES = []


def set_slave_nodes(credentials):
    global SLAVE_NODES
    user = credentials['user']
    password = credentials['password']
    host = credentials['host']
    rpc_port = credentials['rpc_port']
    chain_node = Savoir(user, password, host, rpc_port, "bpchain")
    SLAVE_NODES.append(chain_node)
    LOG.info("Added connection to slave %d", len(SLAVE_NODES))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # pylint: disable=invalid-name
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        set_slave_nodes(json.loads(body.decode('utf-8')))
