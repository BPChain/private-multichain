from bp_orchestrator import orchestrate
from ..implementation.Setup import Setup
from ..implementation.Slave import Slave
from time import sleep

if __name__ == '__main__':
    sleep(7)
    print('-----------starting')
    orchestrate(Setup(), 21000, Slave)
    print('-----------started')

