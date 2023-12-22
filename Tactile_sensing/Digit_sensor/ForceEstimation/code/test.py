from utils import get_test_loader, load_checkpoint
from models import ImageToForce, DepthImageToForce, RGBDToForce, RGBandDToForce, Resnet_modified

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as T

from torchsummary import summary


import argparse
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time


# define the path to load the weights of your model
load_path = "/home/aurova/Desktop/julio/tactile_vision2force/code_deeplearning/weights/training23"

# parameters 
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# value of 1 for debugging
BATCH_SIZE = 1
NUM_WORKERS = os.cpu_count()
PIN_MEMORY = True  # pin_memory speeds up the transfer of the dataset from CPU to GPU during training.


# function to validate the model
def validation_fn(loader, model, loss_fn, train_mode):

	model.eval()

	loop = tqdm(loader)

	running_loss = 0
	test_loss_list = []
	times = []

	with torch.inference_mode():

		for idx, (img, img_depth, rgbd, f) in enumerate(loop):

			# measure t1
			t1 = time.time()

			# forward	
			if train_mode == '0' or train_mode == '4':
				img, f = img.to(DEVICE), f.float().unsqueeze(1).to(DEVICE)
				predictions = model(img)	

			elif train_mode == '1':
				img_depth, f = img_depth.to(DEVICE), f.float().unsqueeze(1).to(DEVICE)
				predictions = model(img_depth)

			elif train_mode == '2':
				rgbd, f = rgbd.to(DEVICE), f.float().unsqueeze(1).to(DEVICE)
				predictions = model(rgbd)

			elif train_mode == '3':
				img, img_depth, f = img.to(DEVICE), img_depth.to(DEVICE), f.float().unsqueeze(1).to(DEVICE)	
				predictions = model(img, img_depth)

			# measure t2
			t2 = time.time()
			print(t2-t1)
			times.append(t2-t1)		

			#img_np = cv2.cvtColor(np.moveaxis(img.detach().cpu().numpy().squeeze(0), 0, -1), cv2.COLOR_BGR2RGB)
			#print(f"Pred force : {predictions.detach().cpu().numpy()}, GT force : {f.detach().cpu().numpy()}")
			#cv2.imshow("img", img_np)
			#cv2.waitKey(1)
			#input()

			loss = loss_fn(predictions, f)
			running_loss += loss.item()
			test_loss_list.append(loss.item())

			loop.set_postfix(loss=loss.item())

	return running_loss/len(loader), test_loss_list, np.array(times)



def main(args):

	test_transform = T.Compose(
		[
		#A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
		T.ToTensor(),
		T.Normalize(
			mean=(0.0),
			std=(1.0),
		),
		],
	)


	test_loader = get_test_loader(
		TEST_IMG_DIR,
		TEST_IMG_DEPTH_DIR,
		TEST_F_DIR,
		test_transform,
		BATCH_SIZE,
		args.train_mode,
		NUM_WORKERS,
		PIN_MEMORY
	)

	# define nn model
	model = None

	if args.train_mode == '0':
		model = ImageToForce().model.to(DEVICE)
		summary(model, (3, 320, 240), device="cuda")
	elif args.train_mode == '1':
		model = DepthImageToForce().model.to(DEVICE)
	elif args.train_mode == '2':
		model = RGBDToForce().model.to(DEVICE)
	elif args.train_mode == '3':
		model = RGBandDToForce().to(DEVICE)
	elif args.train_mode == '4':
		model = Resnet_modified().to(DEVICE)
		summary(model, (3, 320, 240), device="cuda")

	load_checkpoint(torch.load(os.path.join(load_path, "checkpoint_epoch_24.pth.tar")), model)

	loss = nn.L1Loss()


	test_loss, test_loss_list, inf_time = validation_fn(test_loader, model, loss, args.train_mode)
	
	print(len(test_loss_list))
	test_std = np.std(test_loss_list)
	print(f"Test loss: {test_loss} +- {test_std}; Inference time: {np.mean(inf_time)} \n")

	box_plot_dict = plt.boxplot(test_loss_list, showmeans=True)
	print(box_plot_dict['fliers'][0].get_data()[1].shape)
	print(box_plot_dict['boxes'][0].get_data())
	plt.show()



if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--dataset", required=True, type = str, help = 'Dataset format')
	parser.add_argument("-m", "--train_mode", required=True, type = str, help = 'Training mode (nn input)')
	args = parser.parse_args()


	# dataset_sep_objetos or randomize_dataset
	print(args.dataset)
	TEST_IMG_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/data/data/data/datasets/{args.dataset}/test/images"
	TEST_IMG_DEPTH_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/data/data/data/datasets/{args.dataset}/test/img_depth"
	TEST_F_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/data/data/data/datasets/{args.dataset}/test/forces"
	print(TEST_F_DIR)
	main(args)
