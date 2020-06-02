#!/usr/bin/env python
import roslib
import rospy
import sys
from sensor_msgs.msg import Joy
from ackermann_msgs.msg import AckermannDrive
from simple_pid import PID
from cv_bridge import CvBridge, CvBridgeError
import carla
import time
from carla_msgs.msg import CarlaEgoVehicleControl
from controller import VehiclePIDController, PIDLongitudinalController, PIDLateralController


class Ani:
    def __init__(self):
      
        self.veh_pos = None
        # looks for carla on this host
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(2.0)
        # setting world varible for world information
        self.world = self.client.get_world()
        self.actors = self.world.get_actors().filter('vehicle.*')
        self.player = 0
        # self.vehicle = self.world.get_actors().filter('vehicle.audi.etron')[0]	# selecting vehicle for control
        #self.mp = self.world.get_map()

        self.K_P = 0.5
        self.K_I = 0.0
        self.K_D = 0.5         
        
        self.max_speed = 27
        self.max_steering_angle = 170
        self.max_brake = 100
        self.max_reverse = 27

        self.reverse = 0
        self.brake = 0
        self.speed = 0
        self.steering_angle = 0
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.egopub = rospy.Publisher('/carla/ego_vehicle/vehicle_control_cmd', CarlaEgoVehicleControl,
                                      queue_size=1)

    def joy_callback(self, joy_msg):
        self.speed = joy_msg.axes[0] * self.max_speed
        self.steering_angle = joy_msg.axes[3] * self.max_steering_angle
        self.brake = joy_msg.axes[2] * self.max_brake
        self.reverse = joy_msg.axes[5] * self.max_reverse

    def pub_callback(self, msg):

        self.egopub.publish(msg)

    '''def getActor(self):
        for actor in self.actors:
            if actor.attributes.get('role_name') == 'hero':
                player = actor
            break
        return player'''

def main():
    control = Ani()
    rospy.init_node('Carla_manual_control')
    rate = rospy.Rate(10)
    #control.getActor()
    
    for actor in control.actors:
            if actor.attributes.get('role_name') == 'hero':
                control.player = actor
               #print(player)
            break

    # PID speed control parameters
    lon_param = {'K_P': 0.5, 'K_I': 0.5, 'K_D': 0}
    # PID steering control parameters
    lat_param = {'K_P': 1.0, 'K_I': 0.3, 'K_D': 0}
    
    vehicle_controller = VehiclePIDController(
        control.player, lat_param, lon_param)  # variable for the PID controller

    while not rospy.is_shutdown():
        msg = CarlaEgoVehicleControl()
        vehicle_controller.speed = control.speed
        vehicle_controller.steering_angle = control.steering_angle
        vehicle_controller.brake = control.brake
        vehicle_controller.reverse = control.reverse

        msg.throttle = vehicle_controller.speed
        msg.steer = vehicle_controller.steering_angle
        msg.brake = vehicle_controller.brake
        msg.reverse = vehicle_controller.reverse

        control.pub_callback(msg)
        rate.sleep()


if __name__ == '__main__':
    main()
