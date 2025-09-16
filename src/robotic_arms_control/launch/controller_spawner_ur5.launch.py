from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkgPath = get_package_share_directory('robotic_arms_control')
    gazeboLaunchFile = os.path.join(pkgPath, 'launch', 'gazebo_bringup_ur5.launch.py')

    return LaunchDescription([
        # Launch Gazebo with UR5
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazeboLaunchFile)
        ),
        # Spawn joint_trajectory_controller
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_trajectory_controller'],
            output='screen'
        ),
        
        # Spawn joint_state_broadcaster
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
            output='screen'
        ),


    ])
