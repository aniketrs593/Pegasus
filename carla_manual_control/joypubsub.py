#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from nav_msgs.msg import Odometry

# Receive joystick messages (subscribed to Joy topic)
# convert the joysick inputs into Twist commands
# axis 1 is for left stick vertical controls linear speed
# axis 0 is for left stick horizonal controls angular speed
def callback(data):
    twist = Twist()
    # vertical left stick axis = linear rate
    twist.linear.x = 4*data.axes[1]
    # horizontal left stick axis = angular rate
    twist.angular.z = 4*data.axes[0]
    pub.publish(twist)


def main():
    
    global pub
    pub = rospy.Publisher('/carla/ego_vehicle/odometry', Twist, queue_size=10)
    rospy.Subscriber("joy", Joy, callback)
    
    rospy.init_node('joypubsub')
    rospy.spin()

if __name__ == '__main__':
    main()

