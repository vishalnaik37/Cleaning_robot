from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Package paths
    pkg_description = get_package_share_directory('robotic_arms_control')
    urdf_file = os.path.join(pkg_description, "urdf", "ur5.urdf")

    # Read URDF content
    with open(urdf_file, 'r') as f:
        urdf_content = f.read()

    # Correct GAZEBO_MODEL_PATH for Ignition Gazebo
    # Should point to package share folder containing meshes
    os.environ['GAZEBO_MODEL_PATH'] = os.environ.get('GAZEBO_MODEL_PATH', '') + os.pathsep + pkg_description

    # Optional: add gz binary to PATH
    os.environ['PATH'] += os.pathsep + '/opt/ros/jazzy/opt/gz_tools_vendor/bin'

    return LaunchDescription([
        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': urdf_content}]
        ),

        # Launch Ignition Gazebo
        ExecuteProcess(
            cmd=['gz', 'sim', '-v', '4'],
            output='screen'
        ),

        # Spawn robot after 2 seconds to ensure Gazebo is up
        TimerAction(
            period=2.0,
            actions=[
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    name='spawn_ur5',
                    output='screen',
                    arguments=['-topic', '/robot_description', '-name', 'arm']
                )
            ]
        )
    ])
