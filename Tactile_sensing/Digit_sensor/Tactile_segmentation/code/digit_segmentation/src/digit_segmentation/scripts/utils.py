# utils
import os
import torch
import torchvision
from torch.utils.data import DataLoader
from dataset import SegmentationDataset
import pathlib
#mport wandb
import time
import numpy as np


def save_checkpoint(state, epoch, filename="my_checkpoint.pth.tar"):
	print("=> Saving checkpoint")
	filename = f"checkpoint_epoch_{epoch}.pth.tar"
	torch.save(state, f=filename)


def load_checkpoint(checkpoint, model):
	print("=> Loading checkpoint")
	model.load_state_dict(checkpoint["state_dict"])


def get_loaders(
		train_dir,
		train_maskdir,
		val_dir,
		val_maskdir,
		batch_size, 
		train_transform,
		val_transform,
		num_workers=os.cpu_count(),
		pin_memory=True,
):

	train_ds = SegmentationDataset(
			image_dir=train_dir,
			mask_dir=train_maskdir,
			transform=train_transform,
	)

	train_loader = DataLoader(
			train_ds,
			batch_size=batch_size,
			num_workers=num_workers,
			pin_memory=pin_memory,
			shuffle=True,
	)


	val_ds = SegmentationDataset(
			image_dir=val_dir,
			mask_dir=val_maskdir,
			transform=val_transform,
	)

	val_loader = DataLoader(
			val_ds,
			batch_size=batch_size,
			num_workers=num_workers,
			pin_memory=pin_memory,
			shuffle=False,
	)

	return train_loader, val_loader


def dice_iou_calculation(loader, model, loss_fn=None, device="cuda"):

	dice_score = []
	iou_score = []
	running_loss = []
	inf_times = []

	model.eval()

	with torch.inference_mode():

		for idx, (x, y) in enumerate(loader):

			t1 = time.time()

			x, y = x.to(device), y.to(device).unsqueeze(1)

			predictions = model(x)
			#loss = loss_fn(predictions, y)
			#running_loss += loss.item()

			preds = torch.sigmoid(predictions)
			preds = (preds > 0.5).float()

			t2 = time.time()

			inf_times.append(t2-t1)

			intersection = (preds * y).sum()
			union = (preds + y).sum()

			# (preds * y).sum() es la interseccion ; (preds + y).sum() es la union
			dice_score.append((2 * intersection.cpu()) / (union.cpu() + 1e-8))

			iou_score.append(intersection.cpu() / (union.cpu() - intersection.cpu() + 1e-8))

			'''
			if idx == 0:

				for i in range(len(x)):
					images_to_wandb.append([wandb.Image(x[i]), wandb.Image(preds[i]), wandb.Image(y[i])])
			'''
	#table = wandb.Table(data=images_to_wandb, columns=['image', 'pred', 'mask'])
	#wandb.log({"segmentation_images": table})

	dice_score_mean = np.mean(dice_score)
	dice_score_std = np.std(dice_score)
	iou_score_mean = np.mean(iou_score)
	iou_score_std = np.std(iou_score)

	print(inf_times[0])
	inf_times = inf_times[1:]
	mean_inf_times = np.mean(inf_times)
	std_inf_times = np.std(inf_times)

	model.train()

	return 0, dice_score_mean, dice_score_std, iou_score_mean, iou_score_std, mean_inf_times, std_inf_times


def save_predictions_as_imgs(
		loader, model, epoch, folder="saved_images/", device="cuda",
):

	p = pathlib.Path(os.path.join(folder), str(epoch))
	p.mkdir(parents=True, exist_ok=True)

	model.eval()

	for idx, (x, y) in enumerate(loader):
		x = x.to(device)
		with torch.inference_mode():
			preds = torch.sigmoid(model(x))
			preds = (preds > 0.5).float()
		
		
		torchvision.utils.save_image(
				x, f"{folder}/{epoch}/data_{idx}.png"
		)

		torchvision.utils.save_image(
				preds, f"{folder}/{epoch}/pred_{idx}.png"
		)

		torchvision.utils.save_image(y.unsqueeze(1), f"{folder}/{epoch}/true_{idx}.png")

		if idx == 2:
			break

	model.train()

def save_predictions_as_imgs_test(
		loader, model, folder="saved_images_test/", device="cuda",
):

	model.eval()

	with torch.inference_mode():
		for idx, (x, y) in enumerate(loader):
			x = x.to(device)
			
			preds = torch.sigmoid(model(x))
			preds = (preds > 0.5).float()
			
			torchvision.utils.save_image(
				x, f"{folder}/data_{idx}.png"
			)

			torchvision.utils.save_image(
					preds, f"{folder}/pred_{idx}.png"
			)

			torchvision.utils.save_image(y.unsqueeze(1), f"{folder}/true_{idx}.png")


