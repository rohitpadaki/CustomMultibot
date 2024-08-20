import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = "minibot"
    pkg_path = os.path.join(get_package_share_directory(pkg_name), 'launch', 'robot_state_publisher.launch.py')
    gazebo_path = os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    gazebo_params_file = os.path.join(get_package_share_directory(pkg_name),'config','gazebo_params.yaml')
    
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([pkg_path]),
        launch_arguments = {'use_sim_time': 'true'}.items()
    )
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_path]), launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
    )
    
    spawn = Node(
        package = 'gazebo_ros',
        executable = 'spawn_entity.py',
        arguments = ['-topic','robot_description', '-entity', 'amr_bot'],
        output = 'screen'
    )
    
    return LaunchDescription([
        rsp,
        gazebo,
        spawn
    ])