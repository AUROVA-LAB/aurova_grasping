## Touch-based Effector Control for 3D Surface Tracking

This repository provides a tactile-based control method for robotic surface tracking using a Kinova Gen3 robotic arm and a PapillArray tactile sensor. The controller regulates both normal contact force and end-effector orientation, enabling the robot to adapt to unknown 3D surfaces for finishing tasks such as polishing and inspection, with special application in the footwear industry.
Overview available at the link: [Touch-based_3d_surfaces](https://aurova-projects.github.io/Touch-based_3d_surfaces/)

## Docker is all you need

You can also use only Docker to run the package. To do so, follow these simple steps.

### Clone the repository

```bash
git clone https://github.com/AUROVA-LAB/aurova_grasping.git
```

### Build the Docker image

```bash
cd /path/to/your/directory/aurova_grasping/force_control_kinova/
sudo docker build -t kinova_docker .
```

### Run the container

```bash
xhost +local: && sudo docker run --shm-size=1g --privileged --ulimit memlock=-1 \
--ulimit stack=67108864 -it --net=host -e DISPLAY=$DISPLAY --user=root
-v /tmp/.X11-unix:/tmp/.X11-unix:rw
--name kinova_container --cpuset-cpus=0-4 kinova
```

## Run force example (comming soon)


## Acknowledgments
We would like to acknowledge the following repositories for their contributions to this project:

- [Kinova ros-cortex](https://github.com/Kinovarobotics/ros_kortex/tree/noetic-devel)
