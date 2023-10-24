# ROS Package to run DIGIT sensor

This ROS workspace can publish the raw RGB image from the sensor, but also the 3D reconstruction from (https://github.com/vocdex/digit-depth). In my case, to avoid installing torch, cuda, etc., on my computer, I have used conda together with ROS noetic in Python3. Now, I am going to define the steps to create the conda environment and use it to compile the ROS workspace. 

# Create conda env with python3.8
```sh
conda create -n digit_depth python=3.8
```

```sh
conda activate digit_depth
```

# Install libraries from requirements.txt using pip inside of conda env
```sh
pip install -r requirements.txt
```

# Install rospkg and empy libraries with pip inside of conda env to run catkin_make without errors

```sh
pip install rospkg empy
```

# Now, you can compile the ROS workspace with catkin_make
```sh
cd digit_ros
catkin_make
source devel/setup.bash
```

# All right, it's time to run the digit_depth and digit launchs
Digit node publishes the RGB tactile image. Digit_depth subscribes to Digit node to get the image and estimate the 3D.
```sh
roscore
roslaunch digit_interface digit_depth.launch
roslaunch digit_interface digit.launch 
```
