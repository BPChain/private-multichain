from threading import Thread

from ..project_logger import set_up_logging
from .chain_controller_interface import start_controller_server
from .http_server import start_slave_server
from .meta_scenario import run_scenario

LOG = set_up_logging(__name__)




def main():
    Thread(target=start_controller_server, args=[]).start()
    Thread(target=start_slave_server, args=[]).start()
    Thread(target=run_scenario, args=[]).start()
    LOG.info('All threads started')


if __name__ == '__main__':
    main()
