# Demos and resources

https://drive.google.com/drive/folders/1c5mJ4jsSzT3bE7n0Y5BGTtH3gKlKw9Xi?usp=sharing

# Prac 1

## Workspaces involved

prac1_ROS2_ws_humble

## prac1_ROS2_ws_humble

This practice contains a simple text to speech(node_tts.py) and speech to text nodes
This package has been programmed with ROS2 Humble

### Requirements
Install package dependencies executing dependencies.sh script.
If some error with the audio package exists try to install the next dependency

sudo apt update
sudo apt install portaudio19-dev

### Text to speech 

This node listens for text in the /text topic. This text is then processed
by the node and reproduced by one of your audio outputs

How to use:

* Execute tts node in one terminal : ros2 run prac1 node_tts.py

* Public some text in the /text topic :
ros2 topic pub /text std_msgs/msg/String "data: 'Hello world from console'"


### Speech to text

This node just records the microphopne in intervals of 4 sconds and generate the text from the record. 

How to use it :
* ros2 run prac1 node_stt.py
* Spoke to the mic and the interpreted words will appear in the console


# Prac2 

In this practice usb camera images are obtained from a node in ROS1 and then passed to ROS2 through ROS1_bridge package. In the ROS2 node the images are processed to detect if a detected person is wearing a mask.

ROS1 version used is Noetic
ROS2 version used is Galactic

Notice both ROS2 and ROS1 involved workspaces have to be compiled before compile the ROS1_bridge workspace


A docker image is avaliable with all the environment configured to work. https://hub.docker.com/r/imartc04/middleware. 


## Workspaces involved

prac2_bridge_ROS2_ws_galactic/
prac2_ROS1_ws_noetic/
prac2_ROS2_ws_galactic/

## prac2_bridge_ROS2_ws_galactic

This workspace contains a .repos file to import the ROS1_bridge. 
Check documentation in web for installation and how to use it https://github.com/ROS2/ROS1_bridge


## prac2_ROS1_ws_noetic

Just contains the code of the usb_cam package which reads and publish images from the camera.

How to use it : rosrun usb_cam usb_cam_node

## prac2_ROS2_ws_galactic
Contains the package of the mask detection node
The trained and used tensorflow model is in the demos folder
How to use it : ros2 run mask_detector mask_detect_node.py

# Prac 3 

The objetive of this practice is to create a ROS2 action server and client and navigate with nav2 package making use of it in the action server. 
The server client will send individual points to the action server as goals.
The sever offers a service to cancell the process
The version of ROS2 used is Humble

## Workspaces involved

custom_nav_interfaces
imartc_custom_navigator

## custom_nav_interfaces
This package simply creates the action class used by client and server. The package of the custom navigator was not used to create also
its action messages due mix action files with other code stuff generates several problems when compiling

## imartc_custom_navigator
Contains 2 nodes, one for the client and other for the server. Also contains a yaml file with the coordinates of points where to navigate and a launch file that launches everything automatically

How to use it : 
* Install nav2 packages https://navigation.ros.org/getting_started/index.html#installation 
* Set env vars to load gazebo models export TURTLEBOT3_MODEL=waffle && export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models 
* Execute launcher ros2 launch imartc_custom_navigator custom_nav.launch.py
* Call cancel service to stop the robot : ros2 service call /custom_nav_cancel std_srvs/srv/SetBool "{data: true}"



