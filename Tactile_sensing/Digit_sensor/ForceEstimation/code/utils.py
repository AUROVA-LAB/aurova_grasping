# utils
import os
import torch
from torch.utils.data import DataLoader
from load_data import VisionToForceDataset



def save_checkpoint(path, state, epoch, filename="my_checkpoint.pth.tar"):
	print("=> Saving checkpoint")
	filename = f"{path}/checkpoint_epoch_{epoch}.pth.tar"
	torch.save(state, f=filename)


def load_checkpoint(checkpoint, model):
	print("=> Loading checkpoint")
	model.load_state_dict(checkpoint["state_dict"])


def get_loaders(
		train_img_dir,
		train_img_depth_dir,
		train_f_dir,
		val_img_dir,
		val_img_depth_dir,
		val_f_dir,
		batch_size, 
		train_transform,
		val_transform,
		train_mode,
		num_workers=os.cpu_count(),
		pin_memory=True,
		
):

	train_ds = VisionToForceDataset(
			image_dir=train_img_dir,
			img_depth_dir=train_img_depth_dir,
			force_dir=train_f_dir,
			transform=train_transform,
			train_mode=train_mode
	)

	train_loader = DataLoader(
			train_ds,
			batch_size=batch_size,
			num_workers=num_workers,
			pin_memory=pin_memory,
			shuffle=True,
	)


	val_ds = VisionToForceDataset(
			image_dir=val_img_dir,
			img_depth_dir=val_img_depth_dir,
			force_dir=val_f_dir,
			transform=val_transform,
			train_mode=train_mode
	)

	val_loader = DataLoader(
			val_ds,
			batch_size=batch_size,
			num_workers=num_workers,
			pin_memory=pin_memory,
			shuffle=True,
	)

	return train_loader, val_loader


def get_test_loader(
		test_img_dir,
		test_img_depth_dir,
		test_f_dir,
        test_transform,
		batch_size, 
		train_mode,
		num_workers=os.cpu_count(),
		pin_memory=True,
):

	test_ds = VisionToForceDataset(
			image_dir=test_img_dir,
			img_depth_dir=test_img_depth_dir,
			force_dir=test_f_dir,
            transform=test_transform,
			train_mode=train_mode
	)

	test_loader = DataLoader(
			test_ds,
			batch_size=batch_size,
			num_workers=num_workers,
			pin_memory=pin_memory,
			shuffle=False,
	)


	return test_loader

