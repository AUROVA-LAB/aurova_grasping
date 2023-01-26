sudo apt install ros-melodic-pass-through-controllers* ros-melodic-ur-msgs ros-melodic-speed-scaling-state-controller* ros-melodic-speed-scaling-interface ros-melodic-scaled-joint-trajectory-controller* ros-melodic-industrial-robot-status-interface -y


external control UR5e

	roslaunch ur_robot_driver ur5e_bringup.launch robot_ip:=172.18.34.201 kinematics_config:=/home/zalmanpc/ur5e_ws/src/calib.yaml

Ejecutar external control en el robot real en VNC

Planning 
	roslaunch ur5e_moveit_config ur5e_moveit_planning_execution.launch

moveit RVIZ

	roslaunch ur5e_moveit_config moveit_rviz.launch rviz_config:=$(rospack find ur5e_moveit_config)/launch/moveit.rviz






