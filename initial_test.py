import logging
import time
import math

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/40/2M/E7E7E7E7E7')

#global data

setpoint = [1.0, 0.5, 1.0, 0]
err_threshold = .05
step = .1

def wait_for_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms = 500)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_estimator(cf)


def position_callback(timestamp, data, logconf):
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']

def get_pose(scf):
    # A function to get the x y z position data.
    # Could be edited to add yaw or other states.
    log_pos = LogConfig(name='Position', period_in_ms=200)
    log_pos.add_variable('kalman.stateX', 'float')
    log_pos.add_variable('kalman.stateY', 'float')
    log_pos.add_variable('kalman.stateZ', 'float')
    log_pos.data_received_cb.add_callback(position_callback)
    scf.cf.log.add_config(log_pos)

    with SyncLogger(scf, log_pos) as logger:
        for log_entry in logger:
            data = log_entry[1]
            x = data['kalman.stateX']
            y = data['kalman.stateY']
            z = data['kalman.stateZ']
            pose=[x, y, z]
            return x, y, z

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache='./cache')

    with SyncCrazyflie(uri, cf=cf) as scf:
        reset_estimator(scf)
        [x,y,z] = get_pose(scf)
        cf.commander.send_position_setpoint(x, y, .5, 0)
        time.sleep(1)

        keep_flying = True

        while (keep_flying):
            print("still flying")
            VELOCITY = 0.2
            vel_x = 0.0
            vel_y = 0.0
            vel_z=  0.0

            [x, y, z] = get_pose(scf)
            x_err = setpoint[0] - x
            y_err = setpoint[1] - y
            z_err = setpoint[2] - z

            err_mag = math.sqrt(pow(x_err, 2)+pow(y_err, 2)+pow(z_err, 2))

            x_pos = x + (x_err > step) * x_err / err_mag * step + (x_err < step) * x_err
            y_pos = y + (y_err > step) * y_err / err_mag * step + (y_err < step) * y_err
            z_pos = z + (z_err > step) * z_err / err_mag * step + (z_err < step) * z_err

            vel_x = (x_err<=0.5)*x_err+(x_err>0.5)*VELOCITY
            vel_y = (y_err<=0.5)*y_err+(y_err>0.5)*VELOCITY
            vel_z=  (z_err<=0.5)*z_err+(z_err>0.5)*VELOCITY

            keep_flying = (x_err >= err_threshold or 
                y_err >= err_threshold or
                z_err >= err_threshold)

            print('current pos: ({}, {}, {})'.format(x, y, z))
            print('desired pos: ({}, {}, {})'.format(x_pos, y_pos, z_pos)) 
            #cf.commander.send_velocity_world_setpoint(vel_x, vel_y, vel_z, 0) #uncomment for velocity mode OR
            cf.commander.send_position_setpoint(x_pos, y_pos, z_pos, 0) #uncomment for setpoint mode. 

            time.sleep(0.1)

        cf.commander.send_zdistance_setpoint(x, y, .1, 0) #get close to ground before landing
        time.sleep(2)
        cf.commander.send_stop_setpoint()
        print('Setpoint achieved, Demo terminated!')