"""I receive multichain username, password and ip from slave nodes and get their Savoir instances
to control them """

import json
from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus

from python_sources.implementation.Setup import Setup
from .meta_scenario import SLAVES_SYNC
from python_sources.implementation.Slave import Slave

from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)
_SLAVE_NODES = []
SETUP = Setup()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """I handle requests form the slaves who send their user data"""

    # pylint: disable=invalid-name
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        print(body)
        config = json.loads(body.decode('utf-8'))
        self.add_slave_nodes(config)

    def add_slave_nodes(self, config):
        # pylint: disable=global-statement
        global _SLAVE_NODES
        _SLAVE_NODES = [slave for slave in _SLAVE_NODES if slave.is_alive()] + \
                       [Slave.get_new(config, SETUP)]
        LOG.info("Added connection to slave %d", len(_SLAVE_NODES))
        LOG.info(_SLAVE_NODES)
        SLAVES_SYNC.put(_SLAVE_NODES)


def start_slave_server():
    LOG.info("Masternode is ready for connections")
    httpd = HTTPServer(('', 60000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
