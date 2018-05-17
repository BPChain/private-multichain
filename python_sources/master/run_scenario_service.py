"""I run the scenario service"""

from time import sleep

from bp_orchestrator import orchestrate

from ..implementation.setup import Setup
from ..implementation.slave import Slave

if __name__ == '__main__':
    print('-----------starting')
    orchestrate(21000, Slave, Setup())
    print('-----------started')
