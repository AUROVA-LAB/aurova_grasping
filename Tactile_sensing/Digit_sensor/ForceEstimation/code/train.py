import cv2
import numpy as np
import os
from tqdm import tqdm
import argparse
import wandb

from utils import get_loaders, get_test_loader, save_checkpoint
from models import ImageToForce, DepthImageToForce, RGBDToForce, RGBandDToForce, Resnet_modified

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as T

from torchsummary import summary



# wandb settings
os.system("wandb login")
wandb.init(project="digit_contactile_force_final", entity="jcarobotics")


save_path = "/home/aurova/Desktop/julio/tactile_vision2force/code_deeplearning/weights"


BATCH_SIZE = 64
NUM_WORKERS = os.cpu_count()
PIN_MEMORY = True  # pin_memory speeds up the transfer of the dataset from CPU to GPU during training.

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

LEARNING_RATE = 4e-5 #1e-4
NUM_EPOCHS = 25


def define_transformations():

	# with A.Normalize we just divide the pixels by 255 to have them
	# in 0-1 range
	train_transform = T.Compose(
		[
		#A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
		T.ToTensor(),
		T.Normalize(
			(0.0), (1.0)
		),
		
		],
	)

	# never apply augmentations to the validation or test set!
	val_transform = T.Compose(
		[
		#A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
		T.ToTensor(),
		T.Normalize(
			(0.0), (1.0)
		),
		],
	)

	test_transform = T.Compose(
		[
		#A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
		T.ToTensor(),
		T.Normalize(
			(0.0), (1.0)
		),
		],
	)

	return train_transform, val_transform, test_transform



def train_fn(loader, model, optimizer, loss_fn, train_mode):

	# progress bar
	loop = tqdm(loader)

	running_loss = 0

	for batch_idx, (img, img_depth, rgbd, f) in enumerate(loop):
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

		# loss
		loss = loss_fn(predictions, f)
		running_loss += loss.item()


		# zero grad
		optimizer.zero_grad()
		#backward
		loss.backward()
		# update weights
		optimizer.step()

		# update tqdm loop
		loop.set_postfix(loss=loss.item())

	return running_loss/len(loader)


def validation_fn(loader, model, loss_fn, train_mode):

	model.eval()

	loop = tqdm(loader)

	running_loss = 0

	with torch.inference_mode():

		for idx, (img, img_depth, rgbd, f) in enumerate(loop):

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


			loss = loss_fn(predictions, f)
			running_loss += loss.item()

	

			loop.set_postfix(loss=loss.item())

	return running_loss/len(loader)


def main(args):
	

	# save hyper-params in wandb config
	
	'''
	wandb.config = {
		"model_name": args.nninput,
		"learning_rate": LEARNING_RATE,
		"batch_size": BATCH_SIZE,
		"num_epochs": NUM_EPOCHS,
		"optimizer": "adam",
		"loss": "MSE"
	}
	'''

	# define transformations
	train_transform, val_transform, test_transform = define_transformations()
	

	# load data
	train_loader, val_loader = get_loaders(
		TRAIN_IMG_DIR,
		TRAIN_IMG_DEPTH_DIR,
		TRAIN_F_DIR,
		DEV_IMG_DIR,
		DEV_IMG_DEPTH_DIR,
		DEV_F_DIR,
		BATCH_SIZE,
		train_transform,
		val_transform,
		args.train_mode,
		NUM_WORKERS,
		PIN_MEMORY,
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

	# define loss function 
	loss = nn.L1Loss()

	# define optimizer
	optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

	#if args.lrdecay == "True":
	#	scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

	
	# training loop
	for epoch in range(NUM_EPOCHS):

		print(f"-------------Epoch {epoch}-------------")

		# training phase
		train_loss = train_fn(train_loader, model, optimizer, loss, args.train_mode)

		print(f"Training loss: {train_loss} \n")

		# validation phase
		validation_loss = validation_fn(val_loader, model, loss, args.train_mode)

		print(f"Validation loss: {validation_loss} \n")

		# lr decay (optional)
		#if args.lrdecay == "True":
		#	scheduler.step() 

		if args.save == "True":
			checkpoint = {
				"state_dict": model.state_dict(),
				"optimizer": optimizer.state_dict(),
			}
			
			if not os.path.exists(os.path.join(save_path, args.training)):
				os.makedirs(os.path.join(save_path, args.training))
			
			save_checkpoint(os.path.join(save_path, args.training), checkpoint, epoch)


		# wandb logs
		wandb.log({'epoch': epoch+1, 'train_loss': train_loss})
		wandb.log({'epoch': epoch+1, 'validation_loss': validation_loss})
		

	# testing phase
	test_loss = validation_fn(test_loader, model, loss, args.train_mode)
	wandb.log({'epoch': epoch+1, 'test_loss': test_loss})

	print(f"Test loss: {test_loss} \n")



if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	#parser.add_argument("-v", "--vis", required=True, type = str, help = 'True to visualize training samples')
	parser.add_argument("-s", "--save", required=True, type = str, help = 'True to save weights from training')
	parser.add_argument("-t", "--training", required=True, type = str, help = 'Number of training folder')
	parser.add_argument("-m", "--train_mode", required=True, type = str, help = 'Training mode (nn input)')
	parser.add_argument("-d", "--dataset", required=True, type = str, help = 'Dataset format')
	#parser.add_argument("-lrd", "--lrdecay", required=True, type = str, help = 'LR decay')
	args = parser.parse_args()


	TRAIN_IMG_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/train/images"
	TRAIN_IMG_DEPTH_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/train/img_depth"
	TRAIN_F_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/train/forces"
	DEV_IMG_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/dev/images"
	DEV_IMG_DEPTH_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/dev/img_depth"
	DEV_F_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/dev/forces"
	TEST_IMG_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/test/images"
	TEST_IMG_DEPTH_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/test/img_depth"
	TEST_F_DIR = f"/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/{args.dataset}/test/forces"

	print(f"TRAINING WITH DATASET = {args.dataset}")

	main(args)