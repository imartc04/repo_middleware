from launch import LaunchDescription
from launch_ros.actions import Node
import launch
import launch.actions
from launch.actions import IncludeLaunchDescription
import launch.substitutions
import launch_ros.actions
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
import time

def generate_launch_description():

     # Get the path to the package's share directory
    custon_nav_package_path = get_package_share_directory('imartc_custom_navigator')
    
    # Define the parameter file path relative to the package's share directory
    point_yaml = launch.substitutions.LaunchConfiguration('point_yaml', default=[custon_nav_package_path, '/rsc/points.yaml'])
        

    action_server = Node(
        package="imartc_custom_navigator",
        executable="node_action_server.py",
        name="custom_nav_server",
        parameters=[{'init_pos': "-2.0, -0.23, 0.01, 0.99"}],
        output="screen"
        )

    action_client = Node(
            package="imartc_custom_navigator",
            executable="node_action_client.py",
            name="custom_nav_client",
            parameters=[{'point_yaml': point_yaml}],
        output="screen"
        )

    # Define the relative path to the included launch file within the ROS installation directory
    bringup_dir = get_package_share_directory('nav2_bringup')
    launch_dir = os.path.join(bringup_dir, 'launch')
    map_dir = os.path.join(bringup_dir, "maps")

    nav2_tb3_launch = IncludeLaunchDescription( 
    PythonLaunchDescriptionSource( 
            os.path.join(launch_dir, 'tb3_simulation_launch.py')),
        
            launch_arguments={'headless': "False",
                                'map_yaml_file': str(map_dir) + "turtlebot3_world.yaml" 
            }.items()
        )

    
    # Create the launch description and add the node action
    ld = launch.LaunchDescription()
    ld.add_action(nav2_tb3_launch)
    time.sleep(4)
    ld.add_action(action_server)
    time.sleep(4)
    ld.add_action(action_client)

    return ld
