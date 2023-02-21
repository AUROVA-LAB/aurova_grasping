# VISTASE dataset (v1) - VISuo-TActile SEgmentation dataset

This dataset contains tactile images obtained with the vision-based tactile sensor known as Digit when grasping 16 different objects from YCB dataset (see first image), which contains different properties related to touch such as weight, friction, deformation, shape, height, width, etc. This dataset can be used to train and evaluate segmentation neural networks applied to tactile sensing. 

![image1](https://github.com/AUROVA-LAB/aurova_grasping/tree/main/Tactile_sensing/Digit_sensor/Tactile_segmentation/figures/tactile_segmentation_dataset.png?raw=true)



The total number of images is 3675 and there are approximately 200-250 images per object, as can be seen in the next table.

| Object  | Number of images | Object | Number of images
| :-------------: |:-------------:| :-------------: |:-------------:|
| mustard      |     202 | pitcher | 244
| mug      | 223   | screwdriver | 212
| orange      | 240     | scissors | 248
| banana |      218    | mini soccer ball | 237
tomato soup can | 234 | plastic powerdrill | 249
bleach | 238   | clamp | 231
spam meat | 232 | spoon | 201
windex | 239 | tuna can | 227


The following image shows some examples of tactile segmentation where the first row corresponds to the raw tactile images, the second row to the ground truth images and the last row to the segmented contact regions. 

![image2](https://github.com/AUROVA-LAB/aurova_grasping/tree/main/Tactile_sensing/Digit_sensor/Tactile_segmentation/figures/segmentation_examples.png?raw=true)

