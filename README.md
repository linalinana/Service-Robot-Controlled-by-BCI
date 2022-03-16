# Service-Robot-Controlled-by-BCI
A service robot controlled by SSVEP-BCI system

# running program

1. camera command
sudo -s
roslaunch openni2_launch openni2.launch depth_registration:=true

2. yolo
roslaunch darknet_ros darknet_ros.launch

3. robotic_arm command
roslaunch dynamixel arm_grasp.launch

4. contact with EEG, walk and grab the object
roslaunch darknet_ros pcl_box_center.launch
rosrun dynamixel turtle.py
