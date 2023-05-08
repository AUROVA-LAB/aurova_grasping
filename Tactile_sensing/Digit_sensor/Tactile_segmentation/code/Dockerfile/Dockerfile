FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG USER_ID
ARG GROUP_ID

ARG DEBIAN_FRONTEND=noninteractive

RUN pip install albumentations
RUN pip install segmentation-models-pytorch
RUN apt-get update
RUN apt-get install nano

RUN apt-get update && apt-get install -y gnupg

RUN apt-get update && apt-get install -y lsb-release && apt-get clean all

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

RUN apt install curl -y

RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -

RUN apt update

RUN apt install ros-melodic-desktop-full -y

#RUN python3 -m venv /opt/venv

#RUN . /opt/venv/bin/activate && pip install PyYAML && pip install rospkg && pip install empy && pip install opencv-python && pip install opencv-contrib-python

RUN pip install PyYAML && pip install rospkg && pip install empy && pip install opencv-python && pip install opencv-contrib-python

SHELL [ "/bin/bash" , "-c" ]

#RUN source /opt/ros/melodic/setup.bash && mkdir -p catkin_ws/src && cd catkin_ws \
# && catkin_make -DPYTHON_EXECUTABLE:FILEPATH=/opt/conda/bin/python3.7 && source devel/setup.bash \
# && echo "export ROS_MASTER_URI=http://192.168.100.6:11311/" >> /etc/bash.bashrc && cd src && \
# catkin_create_pkg tactile_segmentation std_msgs roscpp rospy && cd tactile_segmentation && mkdir scripts && cd ../.. && catkin_make -DPYTHON_EXECUTABLE:FILEPATH=/opt/conda/bin/python3.7 \
# && source devel/setup.bash
 
