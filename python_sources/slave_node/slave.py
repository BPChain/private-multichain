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
    credentials_sent = False
    while not credentials_sent:
        try:
            conn = http.client.HTTPConnection('masternode', 60000)
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}
            user, password, rpc_port = get_credentials()
            credentials = {'user': user,
                           'password': password,
                           'host': socket.gethostbyname(socket.gethostname()),
                           'rpc_port': rpc_port}
            json_data = json.dumps(credentials)
            conn.request('POST', '/post', json_data, headers)
            credentials_sent = True
        except Exception as error:
            LOG.error(error)
            sleep(5)


if __name__ == '__main__':
    sleep(10)
    send_credentials()
    sleep(60)
