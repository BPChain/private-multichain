import json
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from .meta_scenario import SETTINGS_SYNC


class ControllerInterface(WebSocket):

    def handleMessage(self):
        print(self.data)
        SETTINGS_SYNC.put(json.loads(self.data))



def start_controller_server():
    server = SimpleWebSocketServer('', 20000, ControllerInterface)
    server.serveforever()
