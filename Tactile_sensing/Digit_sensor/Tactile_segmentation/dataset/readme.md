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


# LICENSE AND ACCESS
This dataset is shared only for non-profit research or educational purposes. If you use this dataset or a part of it, please respect these terms of use and reference the original work in which it was published.

# FILE FORMAT
The dataset is structured in 16 folders, one per object. In the paper you can find which object is used for each subdataset for training, validation and testing. The object's folders are organized with the following structure:

    object/
        image_label/
            imageidx_sensorunit.png --> raw images from the Digit sensor.
            labelidx_sensorunit.json --> labeled image in json format.
        
        voc_format/
            class_names.txt --> We do not classify the images, but it is necessary to label all the masks with the same class. After that, we do not use this class for anything.
            JPEGImages/ --> contain the same images as image_label but in jpg format.
                imageidx_sensorunit.png
            SegmetationClass/ 
                labelidx_sensorunit.npy --> contour points saved in npy format.
            SegmentationClassPNG/
                labelidx_sensorunit.png --> black and white labeled images. We used this images for the training, validation and testing.
            SegmentationClassVisualization/
                labelidx_sensorunit.png --> visualization of the masks in the original images.
                

# RELATED PUBLICATIONS (CITATION)
Please, if you use this dataset or part of it, cite the following publication:


    @unpublished{tactiledataset,
    author = {J. Castaño-Amorós, and P. Gil},
    title = { Measuring Object Rotation via Visuo-Tactile Segmentation of Grasping Region },
    note = {Submitted to IEE Robotics and Automation Letters},
    year = {N.D.},
}
  
This research was funded by the Valencian Regional Government through the PROMETEO/2021/075 project and by the University of Alicante through the grant UAFPU21-26.