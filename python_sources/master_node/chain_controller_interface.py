"""I offer the interface for the the chain controller to send me data"""
import json
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from .meta_scenario import SETTINGS_SYNC


# pylint: disable= too-few-public-methods
class ControllerInterface(WebSocket):

    # pylint: disable=invalid-name
    def handleMessage(self):
        print(self.data)
        SETTINGS_SYNC.put(json.loads(self.data))


def start_controller_server():
    server = SimpleWebSocketServer('', 20000, ControllerInterface)
    server.serveforever()
