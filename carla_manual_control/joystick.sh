#!/bin/bash

#read -p "Enter Username: "  username 
#echo "Welcome $username!" &
#sleep 3

xterm -e  "bash ~/CARLA_0.9.8/CarlaUE4.sh" &
sleep 5

xterm  -e  " source ~/CARLA_0.9.8/ros-bridge/devel/setup.bash; roslaunch carla_ros_bridge carla_ros_bridge_with_rviz.launch" & 
sleep 3

xterm  -e  "cd ~/CARLA_0.9.8/PythonAPI/util/; ./config.py -m Town04 --weather ClearNoon" & 
sleep 3

xterm  -e  " source ~/CARLA_0.9.8/ros-bridge/devel/setup.bash; roslaunch carla_ego_vehicle carla_example_ego_vehicle.launch" &
sleep 3

xterm  -e  "rosrun joy joy_node " &
sleep 3

#xterm  -e  " source ~/CARLA_0.9.8/ros-bridge/devel/setup.bash; python joypubsub.py" &
#sleep 3

xterm  -e  " source ~/CARLA_0.9.8/ros-bridge/devel/setup.bash; python manual2.py" &
sleep 3
