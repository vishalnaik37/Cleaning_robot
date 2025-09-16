from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    urdf_file = LaunchConfiguration('urdf_file', default='/home/vishal/UR5_robot/src/robotic_arms_control/robotic_arms_control/urdf/ur5.urdf')
    param_file = LaunchConfiguration('param_file', default='/home/vishal/UR5_robot/src/robotic_arms_control/robotic_arms_control/config/ur5_itc_controller.yaml')

    return LaunchDescription([

        # Launch Gazebo empty world
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '/opt/ros/humble/share/gazebo_ros/worlds/empty.world', '-slibgazebo_ros_init.so', '-slibgazebo_ros_factory.so'],
            output='screen'
        ),

        # Launch robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': urdf_file}]
        ),

        # Timer to wait 5 seconds for Gazebo and robot_state_publisher to be ready
        TimerAction(
            period=5.0,
            actions=[

                # Spawn joint_state_broadcaster
                Node(
                    package='controller_manager',
                    executable='spawner',
                    arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
                    output='screen'
                ),

                # Spawn joint_trajectory_controller
                Node(
                    package='controller_manager',
                    executable='spawner',
                    arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager', '--param-file', str(param_file)],
                    output='screen'
                ),
            ]
        )
    ])
