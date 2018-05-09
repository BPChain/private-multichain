from bp_orchestrator import orchestrate
from ..implementation.Setup import Setup
from ..implementation.Slave import Slave
from time import sleep

if __name__ == '__main__':
    sleep(10)
    print('-----------starting')
    orchestrate(21000, Slave, Setup())
    print('-----------started')

