"""I send my multichain username and password and my ip to a master node so he can control my local
multichan instance """

import http.client
import json
import socket
from time import sleep

from ..data_acquisition.data_acquisition import read_user_and_password, read_rpc_port
from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)

def get_credentials():
    user, password = read_user_and_password()
    return user, password, read_rpc_port()

def send_credentials():
    conn = http.client.HTTPConnection('masternode', 60000)
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}
    user, password, rpc_port = get_credentials()
    foo = {'user': user, 'password': password, 'rpc_port': rpc_port, 'host': socket.gethostbyname(socket.gethostname())
 }
    json_data = json.dumps(foo)

    conn.request('POST', '/post', json_data, headers)

    response = conn.getresponse()
    print(response.read().decode())

if __name__ == '__main__':
    send_credentials()
    sleep(60)
