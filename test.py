from cflib.crazyflie import Crazyflie

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
import logging

# Crazyflie URI
uri = "radio://0/70/2M/E7E7E7E7E7"

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)





if __name__ == "__main__":
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:

        simple_log(scf, lg_stab)

