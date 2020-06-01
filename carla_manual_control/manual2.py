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


class Ani:
    def __init__(self):

        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(2.0)

        self.max_speed = 50
        self.max_steering_angle = 1

        self.speed = 0
        self.steering_angle = 0
        self.brake = 0

        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.egopub = rospy.Publisher('/carla/ego_vehicle/vehicle_control_cmd', CarlaEgoVehicleControl,
                                      queue_size=1)

    def joy_callback(self, joy_msg):
        self.speed = joy_msg.axes[0] * self.max_speed
        self.steering_angle = joy_msg.axes[3] * self.max_steering_angle
        self.brake = joy_msg.axes[5] 

    def pub_callback(self, msg):

        self.egopub.publish(msg)


def main():
    ack = Ani()
    rospy.init_node('Carla_control')
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        cmd_msg = AckermannDrive()
        msg = CarlaEgoVehicleControl()

        while(ack.brake == 1):
            cmd_msg.speed = ack.speed
            cmd_msg.steering_angle = ack.steering_angle
            msg.steer = cmd_msg.steering_angle
            if cmd_msg.speed > 0:
                msg.throttle = cmd_msg.speed
        
            elif cmd_msg.speed < 0:
                msg.reverse = 27
        
        while(ack.brake == -1):
            cmd_msg.speed = ack.speed
            cmd_msg.steering_angle = ack.steering_angle
            msg.steer = cmd_msg.steering_angle
            msg.brake = True
        
    ack.pub_callback(msg)
    rate.sleep()

if __name__ == '__main__':
    main()
