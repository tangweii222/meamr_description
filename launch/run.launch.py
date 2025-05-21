import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = FindPackageShare(package='meamr_description').find('meamr_description')
    default_model_path = os.path.join(pkg_share, 'urdf', 'meamr.urdf.xacro')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz', 'urdf_display.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            name='gui',
            default_value='True',
            description='Use joint_state_publisher_gui'),
        DeclareLaunchArgument(
            name='model',
            default_value=default_model_path,
            description='Absolute path to robot urdf (xacro) file'),
        DeclareLaunchArgument(
            name='rvizconfig',
            default_value=default_rviz_config_path,
            description='Absolute path to RViz config file'),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            condition=UnlessCondition(LaunchConfiguration('gui'))
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            condition=IfCondition(LaunchConfiguration('gui'))
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', LaunchConfiguration('model')])
            }]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            condition=IfCondition(LaunchConfiguration('gui')),
            arguments=['-d', LaunchConfiguration('rvizconfig')]
        )
    ])
