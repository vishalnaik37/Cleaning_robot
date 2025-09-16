from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the path to the package and URDF file
    pkg_description = get_package_share_directory('robotic_arms_control')
    urdf_file = os.path.join(pkg_description, "urdf", "ur5.urdf")


    # Read the URDF file
    with open(urdf_file, 'r') as file:
        urdf_content = file.read()

    # Robot State Publisher (publishes TF and /robot_description)
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{'robot_description': urdf_content}]
    )

    # Joint State Publisher GUI (for moving joints manually)
    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher",
        output="screen"
    )

    # RViz2
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz_gui",
        output="screen"
    )
    
    # Return LaunchDescription
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])
