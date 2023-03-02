import logging
import time
import math

# import cflib things
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils import uri_helper

# import from our files wheeee
import pos_estimator as es

# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/50/2M/E7E7E7E7E7')

# global data
setpoint = [1.0, 0.5, 1.0, 0]
err_threshold = .05
step = .1

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# CALCULATE TRAJECTORY HERE
# something something bogo path
# given setpoint, return trajectory
generated_path = [[.5, 0], [.5, .5], [1, .5]]

# whatever A* thing exists will probably make a 2D path
# let's take that and put it into the format we need for the next part
trajectory = []
for point in generated_path:
    trajectory.append([point[0], point[1], setpoint[2], 0])

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache='./cache')

    with SyncCrazyflie(uri, cf=cf) as scf:
        es.reset(scf)
        [x,y,z] = es.get_pose(scf)

        # so generally speaking, we're starting on the ground.
        # let's make it a 2D problem and go to our height right away
        trajectory.insert(0, [x, y, setpoint[2], 0])

        first_point = True

        for next_point in trajectory:

            [x,y,z] = es.get_pose(scf)

            '''if not first_point:
                next_point = [next_point2[0], next_point2[1], 1, 0]
            else:
                next_point = next_point2[:]'''

            print(f"going to: {next_point}")
            # es.reset(scf)
            

            cf.commander.send_position_setpoint(x, y, z, 0)
            time.sleep(1)

            keep_flying = True

            while (keep_flying):
                print("still flying")
                VELOCITY = 0.1
                vel_x = 0.0
                vel_y = 0.0
                vel_z=  0.0

                [x, y, z] = es.get_pose(scf)

                x_err = next_point[0] - x
                y_err = next_point[1] - y
                z_err = next_point[2] - z

                err_mag = math.sqrt(pow(x_err, 2)+pow(y_err, 2)+pow(z_err, 2))

                x_pos = x + (x_err > step) * x_err / err_mag * step + (x_err < step) * x_err
                y_pos = y + (y_err > step) * y_err / err_mag * step + (y_err < step) * y_err
                z_pos = z + (z_err > step) * z_err / err_mag * step + (z_err < step) * z_err

                vel_x = (x_err <= 0.5) * x_err + (x_err > 0.5) * VELOCITY
                vel_y = (y_err <= 0.5) * y_err + (y_err > 0.5) * VELOCITY
                if first_point:
                    vel_z = (z_err <= 0.5) * z_err + (z_err > 0.5) * VELOCITY

                keep_flying = (x_err >= err_threshold or 
                    y_err >= err_threshold or
                    (z_err >= err_threshold) and first_point)

                print('current pos: ({}, {}, {})'.format(x, y, z))
                print('desired pos: ({}, {}, {})'.format(x_pos, y_pos, z_pos)) 

                cf.commander.send_velocity_world_setpoint(vel_x, vel_y, vel_z, 0) # uncomment for velocity mode OR
                # cf.commander.send_position_setpoint(x_pos, y_pos, z_pos, 0) # uncomment for setpoint mode. 

                time.sleep(0.1)

            
            first_point = False

            
            
        cf.commander.send_zdistance_setpoint(x, y, .1, 0) #get close to ground before landing
        time.sleep(2)
        cf.commander.send_stop_setpoint()
        print('Setpoint achieved, Demo terminated!')
