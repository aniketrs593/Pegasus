# Pegasus
WMUxCSU-IAC 


# Western Michigan University
The purpose of this repository is to control the ego vehicle with a joystick controller.  
** ***NOTE: The controller that are compatible to run this repository is an Xbox controller or a Logitech F310 Controller, Playstation controllers will not work*** **  

** **ANOTHER NOTE: Controlling the car right now with the joystick is unrealistic and we are working on adding more parameters and restrictions to drive the car more realistic** **

## 1. Carla_0.9.8 setup

For custom rosbridge Carla setup visit: 
<https://github.com/nickgoberville/carla-ros-bridge>

## 2. Carla manual control using xbox controller
To setup controller visit: 
<http://wiki.ros.org/joy/Tutorials/WritingTeleopNode>

## 3. Clone Repository and run bash
```
# Connect you controller

# clone the repository
$ cd CARLA_0.9.8/ros-bridge/src
$ git clone https://github.com/aniketrs593/Pegasus.git

# make joypubsub file executable
$ cd carla_manual_control 
$ chmod +x joypubsub.py
$ chmod +x joystick.sh

# Launch joystick bash file
$ ./joystick.sh
```
## Troubleshoot 
if `$ xterm command is not found`, run `$ sudo apt-get install -y xterm` in another terminal and re-run joyStick bash file.



  



