# Pegasus
WMUxCSU-IAC 


# Western Michigan University

# 1. Carla_0.9.8 setup

Custom rosbridge for Carla setup visit : 
<https://github.com/nickgoberville/carla-ros-bridge>

# 2. Manual Control for Carla using xbox controller

## Controller setup:
   
  ## Installing
     sudo apt-get install ros-melodic-joy
   
  ## check connection
     $ ls /dev/input/js0
     output:
     /dev/input/js0
   
  ## check if all buttons are working
     $ sudo jstest /dev/input/js0
     output similar to:
     Driver version is 2.1.0.
     Joystick (Logitech Logitech Cordless RumblePad 2) has 6 axes (X, Y, Z, Rz, Hat0X, Hat0Y)
     and 12 buttons (BtnX, BtnY, BtnZ, BtnTL, BtnTR, BtnTL2, BtnTR2, BtnSelect, BtnStart, BtnMode, BtnThumbL, BtnThumbR).
     Testing ... (interrupt to exit)
     Axes:  0:     0  1:     0  2:     0  3:     0  4:     0  5:     0 Buttons:  0:off  1:off  2:off  3:off  4:off  5:off          6:off  7:off  8:off  9:off 10:off 11:off
    
  ## Making joystick available to ROS joy node
     $ ls -l /dev/input/js0
     Output:
     crw-rw-XX- 1 root dialout 188, 0 2009-08-14 12:04 /dev/input/jsX
     
     If XX is rw: the js device is configured properly.
     If XX is --: the js device is not configured properly and you need to:
     
     $ sudo chmod a+rw /dev/input/jsX
  
 ## Starting joy node:
     $ roscore
     $ rosrun joy joy_node
 ### output similar to: 
     [ INFO] 1253226189.805503000: Started node [/joy], pid [4672], bound on [aqy], xmlrpc port [33367], tcpros port [58776],      logging to [/u/mwise/ros/ros/log/joy_4672.log], using [real] time[ INFO] 1253226189.812270000: Joystick device:              /dev/input/js0 [ INFO] 1253226189.812370000: Joystick deadzone: 2000
     

  



