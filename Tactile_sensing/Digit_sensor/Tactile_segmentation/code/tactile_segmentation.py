#!/opt/conda/bin/python3.7

# -------------- IMPORTS ----------------

# ros imports
import rospy
from sensor_msgs.msg import Image

# general imports
import cv2
import numpy as np
from math import atan2, pi
from collections import deque
import sys
import argparse
import time

# deep learning imports
import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import DataLoader


# -------------- DEFINITION ----------------
# image -> to read the image from digit ros topic.
image = None

# image_height and width to feed the neural network.
IMAGE_HEIGHT = 320
IMAGE_WIDTH = 256  
# device -> gpu if it is possible, cpu otherwise.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# window value to calculate angles; save 2 images, calculate 2 angles,
# then calculate the mean of these two angles.
DYNAMIC_WINDOW = 2


# -------------- ARG PARSER ----------------
parser = argparse.ArgumentParser()
# this arg is used to indicate if the angle calculation is wanted or not.
parser.add_argument('-a', '--angles', type=str, help='1 to calculate angles, 0 otherwise.', 
                    required=True, default=0, choices=['0', '1'])
args = parser.parse_args()


# -------------- PATH DEFINITION FOR NEURAL NETWORKS ----------------
#TODO: upload the scripts to github and then git clone in the dockerfile to
# have these scripts in the docker container per default. 
sys.path.append("../../../../../julio/segmentacion/")
from models import UnetPlusPlus, PSPNet, DeepLabV3Plus
from utils import load_checkpoint


def callback(msg):
    '''
        callback function: is called when a ros node publishes in digit55/camera/image_color
        arguments:
            -input:
                -msg: ros Image msg containing the digit image.
            -output:
                -None
    '''
    global image
    # this line substitutes cvbridge
    image = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)


def config_segmentation_model():
    '''
        config_segmentation_model function: is used to defined and load
        the segmentation model, weights and data augmentation.
        arguments:
            -input:
                -None
            -output:
                -model: torch model with the architecture and loaded weights.
                -test_transform: function with the data augmentation transformations.
    '''

    # load PSPNet model from segmentation_models_pytorch library
    model = PSPNet("resnet18", "imagenet", in_channels=3, out_channels=1).to(DEVICE)

    # load weights
    #TODO: upload weights to github and the git clone to have the weights
    # in the docker container per default.
    load_checkpoint(torch.load("epoch_29.pth.tar"), model)

    # define resize, normalize and tensor convertion with albumentations library.
    test_transform = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0  # value you want to divide by the pixels
            ),
            ToTensorV2(),
        ]
        )

    return model, test_transform


def tactile_segmentation(img_rgb, model, test_transform):

    '''
        tactile_segmentation function: this function predicts the mask from 
        the digit image.
        arguments:
            -input:
                -img_rgb: input image from digit sensor
                -model: torch segmentation model
                -test_transform: function with data augmentation transf.
            -output:
                -pred_mask: predicted mask of the area of contact.
    '''

    # apply the data augmentation transformations
    img_rgb = test_transform(image=img_rgb)
    # get the image
    img_rgb = img_rgb["image"]

    # send the image to device
    img_rgb = img_rgb.to(DEVICE).unsqueeze(0)
    # forward and get the predicted mask
    pred = torch.sigmoid(model(img_rgb))
    pred = (pred > 0.7).float()
    
    # send the mask back from the device and convert to numpy
    pred_np = pred.cpu().detach().numpy()
    # transform the mask to uint8 type and values between 0-255 
    # to visualize it
    pred_mask = pred_np[0][0].astype(np.uint8)*255

    return pred_mask


def config_var_angles():
    '''
        config_var_angles function: this function is used only to clear
        the main function. Here we define the variables needed to perform
        the angle calculation from the pred_mask.
        arguments:
            -input:
                -None
            -output:
                -black_image: image full of black pixels to use it later.
                -acc_angles: deque object to accumulate angles depending
                    on the DYNAMIC_WINDOW value.
                -angles_mean: value to save the mean from acc_angles.
                -first_iter: bool used to save the first angle as the reference.
                -angle_reference: angle value used as the reference to calculate
                    the angle interval.
    '''
    black_image = np.zeros((320, 256), dtype=np.uint8)
    acc_angles = deque()
    angles_mean = 0
    first_iter = True
    angle_reference = 0

    return black_image, acc_angles, angles_mean, first_iter, angle_reference


def calculate_angles(pred_mask, black_image, acc_angles, angles_mean, first_iter, angle_reference):

    '''
        calculate_angles function: this function calculates the skeleton of the mask,
            and calculate the angle of that skeleton (is a line).
        arguments:
            -input:
                -pred_mask: predicted mask of the area of contact.
                -black_image: image full of black pixels to use it later.
                -acc_angles: deque object to accumulate angles depending
                    on the DYNAMIC_WINDOW value.
                -angles_mean: value to save the mean from acc_angles.
                -first_iter: bool used to save the first angle as the reference.
                -angle_reference: angle value used as the reference to calculate
                    the angle interval.
            -output:
                -dif_angle: the interval angle between the current angle and 
                the reference.
    '''

    # get the mask contour
    contours, _ = cv2.findContours(pred_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    dif_angle = 0

    # if there is at least one contour
    if len(contours) > 0:
        # sort contours to get the biggest (mask contour)
        sorted_contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    
        # fit an ellipse to the mask contour
        ellipse = cv2.fitEllipse(sorted_contours[0])
        # draw the ellipse in the black image
        cv2.ellipse(black_image, ellipse, (255,255,255), -1)
        # apply skeleton algorithm to get the major axis of the ellipse
        black_image = cv2.ximgproc.thinning(black_image, thinningType=cv2.ximgproc.THINNING_GUOHALL)
        # get the contour of the axis
        contours_skelet, _ = cv2.findContours(black_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # if the contour is found
        if len(contours_skelet) > 0:

            # fit a line in the axis contour
            [vx,vy,x,y] = cv2.fitLine(contours_skelet[0], cv2.DIST_L2,0,0.01,0.001)
            # calculate the angle with the atan2 function
            mask_line = np.array([vx, vy])
            angle = atan2(mask_line[1], mask_line[0])*180/pi

            # accumulate angles
            acc_angles.append((angle))
            
            # when acc_angle contains DYAMIC_WINDOW values, calculate the angle mean
            # and the interval angle
            if len(acc_angles) == DYNAMIC_WINDOW:
                angles_mean = np.mean(acc_angles)
                
                if not first_iter:
                    dif_angle = abs(angles_mean - angle_reference)
                    
                else:
                    angle_reference = np.mean(acc_angles)
                    first_iter = False

                # delete first image [t-2, t-1] -> [t-1] -> acc_angle.append -> [t-1, t]
                acc_angles.popleft()
            
            cv2.imshow("skeleton", black_image)
    
    return dif_angle


def main():

    # define ros node and subscribe to digit topic
    rospy.init_node("digit_ros_node_read", anonymous=True)
    sub = rospy.Subscriber("/digit55/camera/image_color", Image, callback)

    # set model and data aug transformations
    model, test_transform = config_segmentation_model()

    # define variables in case the angle calculation is wanted
    if args.angles:
        black_image, acc_angles, angles_mean, first_iter, angle_reference = config_var_angles()
    
    # infinite loop
    while True:

        # if the digit image is ready
        if image is not None:
            # conver to rgb to feed the model
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
            # evaluation mode
            model.eval()
            with torch.inference_mode():
                
                t1 = time.time()
                # forward pass
                pred_mask = tactile_segmentation(img_rgb, model, test_transform)
                cv2.imshow("window", pred_mask)
                t2 = time.time()
                # angle calculation
                if args.angles:
                    dif_angle = calculate_angles(pred_mask,
                                                 black_image,
                                                 acc_angles,
                                                 angles_mean,
                                                 first_iter,
                                                 angle_reference)
                t3 = time.time()

                print(f"Net inference time: {(t2-t1)}")
                print(f"Angle inference time: {(t3-t2)}")


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



if __name__ == '__main__':
    main()