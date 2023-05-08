# utils
import os
from tabnanny import filename_only
import torch
import torchvision
from torch.utils.data import DataLoader
from dataset import SegmentationDataset
import pathlib
import wandb


def save_checkpoint(state, epoch, model_name, dataset_number, backbone):
	print("=> Saving checkpoint")
	filename = f"/julio/doctorado/primeranyo/digit/segmentacion/main_folder/experiments/{model_name}/dataset{dataset_number}/{backbone}/epoch_{epoch}.pth.tar"
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


def dice_iou_calculation(loader, model, loss_fn, device="cuda"):

	dice_score = 0
	iou_score = 0
	running_loss = 0
	images_to_wandb = []

	model.eval()

	with torch.inference_mode():

		for idx, (x, y) in enumerate(loader):

			x, y = x.to(device), y.to(device).unsqueeze(1)

			predictions = model(x)
			loss = loss_fn(predictions, y)
			running_loss += loss.item()

			preds = torch.sigmoid(predictions)
			preds = (preds > 0.5).float()

			intersection = (preds * y).sum()
			union = (preds + y).sum()
			# (preds * y).sum() es la interseccion ; (preds + y).sum() es la union
			dice_score += (2 * intersection) / (union + 1e-8)

			iou_score += intersection / (union - intersection + 1e-8)

			if idx == 0:

				for i in range(len(x)):
					images_to_wandb.append([wandb.Image(x[i]), wandb.Image(preds[i]), wandb.Image(y[i])])
	
	table = wandb.Table(data=images_to_wandb, columns=['image', 'pred', 'mask'])
	wandb.log({"segmentation_images": table})

	model.train()

	return running_loss/len(loader), dice_score/len(loader), iou_score/len(loader)


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


