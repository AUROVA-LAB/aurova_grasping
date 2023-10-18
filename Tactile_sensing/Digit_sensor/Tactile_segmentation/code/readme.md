This folder contains the code implemented for our last work with DIGIT sensors. Our work consists of a two-stage system that estimates the angle of rotation of a grasped object when slippage occurs. 

Here we can find two subfolders: a folder that contains the dockerfile file, and another folder which is a catkin workspace containing all the code to run.

First of all, you need to clone the repository in order to later build the docker image. To do it, run cd command until Dockerfile folder and run:

```sh
docker build -t docker_image_name .
```

Once the docker image is built, these two commands have to be executed in the same terminal in order to start the docker container:

```sh 
xhost +
```

```sh 
docker run --net=host  --gpus "all" --rm -it --name docker_container_name --volume path/to/aurova_grasping/Tactile_sensing/Digit_sensor/Tactile_segmentation/code/digit_segmentation:/digit_segmentation -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-uni docker_image_name

```

The docker container with the catkin workspace is already running. Now, run cd to inside the workspace folder, where you need to run these commands:

```sh 
source /opt/ros/melodic/setup.bash
```

```sh 
source devel/setup.bash
```

Now, you can run roscore and the tactile_segmentation.py script with -r 1 flag to apply angle estimation, or 
with -t 1 for centroid translation:

```sh 
cd src/digit_segmentation/scripts/
```

```sh 
python tactile_segmentation.py -r 1 -t 0
```

```sh 
python tactile_segmentation.py -r 0 -t 1
```

The tactile_segmentation.py script will download the weights of ResNet18 neural architecture and will wait until another script will publish a DIGIT image in /digit55/camera/image_color topic.  


# Related publications

J. Castaño-Amorós and P. Gil, "Measuring Object Rotation via Visuo-Tactile Segmentation of Grasping Region," in IEEE Robotics and Automation Letters, vol. 8, no. 8, pp. 4537-4544, Aug. 2023, doi: 10.1109/LRA.2023.3285471.

J. Castano-Amoros and P. Gil, "Rotational Slippage Prediction from Segmentation of Tactile Images", in ViTac Workshop: Blending Virtual and Real Visuo-Tactile Perception (ICRA), London, UK, 2023, arxiv: https://arxiv.org/abs/2305.04660

Citation:

@ARTICLE{10149493,
  author={Castaño-Amorós, Julio and Gil, Pablo},
  journal={IEEE Robotics and Automation Letters}, 
  title={Measuring Object Rotation via Visuo-Tactile Segmentation of Grasping Region}, 
  year={2023},
  volume={8},
  number={8},
  pages={4537-4544},
  doi={10.1109/LRA.2023.3285471}}

@misc{castanoamoros2023rotational,
      title={Rotational Slippage Prediction from Segmentation of Tactile Images}, 
      author={Julio Castano-Amoros and Pablo Gil},
      howpublished={\url{https://arxiv.org/abs/2305.04660}},
      year={2023},
}
