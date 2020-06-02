#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from ackermann_msgs.msg import AckermannDrive
from simple_pid import PID
from cv_bridge import CvBridge, CvBridgeError
import carla
#from nav_msgs.msg import Odometry
#from geometry_msgs.msg import Twist

ack_publisher = None
max_speed = 27  #m/s
max_steering = 170  #radians

def joyCallback(msg):
    for i in range(len(msg.axes)):
        if msg.axes[i] == 1:
            print 'Axis' + str(i) + 'in use !'
    ack_msg = AckermannDrive()
    ack_msg.steering_angle = msg.axes[3] * max_steering
    ack_msg.speed = msg.axes[1] * max_speed
    ack_msg.acceleration = 0.0
    ack_msg.jerk = 0.0
    ack_publisher.publish(ack_msg)
    rate.sleep()

def main():
    global ack_publisher, rate
    rate = rospy.Rate(10)
    rospy.init_node('drive_cmd')
    max_speed = rospy.get_param("~max_speed", 27)
    max_steering = rospy.get_param("~max_steering", 170)
    rospy.Subscriber('joy', Joy, joyCallback)
    ack_publisher = rospy.Publisher('/carla/ego_vehicle/ackermann_cmd', AckermannDrive, queue_size=1)
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    main()



