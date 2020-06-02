#!/usr/bin/env python

import roslib
import sys
import rospy
import numpy as np
import carla
#import newlane

from cv_bridge import CvBridge, CvBridgeError
from matplotlib import pyplot as plt
from sensor_msgs.msg import Image
from carla_msgs.msg import CarlaEgoVehicleControl
from controller import VehiclePIDController

class Brown(object):
	# labeling varibales in the class and to initiate carla information and libraries. 
    def __init__(self):        
        self.veh_pos = None
        self.client = carla.Client('localhost', 2000)	# looks for carla on this host
        self.client.set_timeout(2.0)	# the time in secs it waits before connection 
        self.world = self.client.get_world()	# setting world varible for world information
        self.vehicle = self.world.get_actors().filter('vehicle.tesla.cybertruck')[0]	# selting what vehicle to use for control
        self.mp = self.world.get_map()

        rospy.init_node('Carla_control')	# creating a node in ros

        self.Control()	# calling the control function in the class


    # actor function to get the vehicles waypoints of its path and     
    def Actor(self):
        
        self.veh_pos = self.mp.get_waypoint(self.vehicle.get_location())	# getting vehicle location and waypoints for that route
    
    # controls the vehicles PID steering and speed of the vehicle
    def Control(self):
    	
        rate = rospy.Rate(10)	# setting the rate in Hz of inforation sent to ros
        lon_param = {'K_P':0.5,'K_I': 0.5,'K_D': 0}	# PID speed control parameters
        lat_param = {'K_P':1.0,'K_I': 0.3,'K_D': 0}	# PID steering control parameters
        vehicle_controller = VehiclePIDController(self.vehicle, lon_param, lat_param) # varible for the PID controller
    	'''
		while ros is running this will control the vehicle using the vehicle control command in carla
		then publishes the vehicle contol command through ros to control the vehicle in carla 
    	'''
        while not rospy.is_shutdown():
            self.Actor()
            control = vehicle_controller.run_step(50, self.veh_pos.next(10)[0])
            
            msg = CarlaEgoVehicleControl()
            msg.throttle = control.throttle
            msg.steer = control.steer
            msg.brake = control.brake
            msg.hand_brake = control.hand_brake
            msg.reverse = control.reverse
            msg.gear = 1
            msg.manual_gear_shift = control.manual_gear_shift
            #print(msg) 
            self.Publisher(msg)
            rate.sleep()

    # function to publish the vehicle control command 
    def Publisher(self, msg):
        publisher = rospy.Publisher('/carla/ego_vehicle/vehicle_control_cmd',\
                CarlaEgoVehicleControl, queue_size=1)
        publisher.publish(msg)

# call the calsses
if __name__ == '__main__':
    try:
          Brown()  	
    except KeyboardInterrupt:
        print("Press Crtl-C to terminate while statement")
        pass
