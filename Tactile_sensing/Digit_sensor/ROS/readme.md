# ROS Package to run DIGIT sensor

This ROS workspace can publish the raw RGB image from the sensor, but also the 3D reconstruction from (https://github.com/vocdex/digit-depth). In my case, to avoid installing torch, cuda, etc., on my computer, I have used conda together with ROS noetic in Python3. Now, I am going to define the steps to create the conda environment and use it to compile the ROS workspace. 

# Create conda env with python3.8
´´´conda create -n digit_depth python=3.8

conda activate digit_depth
´´´
