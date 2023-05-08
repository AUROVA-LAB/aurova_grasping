# class to load our dataset
import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np

class SegmentationDataset(Dataset):
  def __init__(self, image_dir, mask_dir, transform=None):
    self.image_dir = image_dir
    self.mask_dir = mask_dir
    self.transform = transform
    self.images = os.listdir(image_dir)

  
  def __len__(self):
    return len(self.images)

  def __getitem__(self, index):

    img_path = os.path.join(self.image_dir, self.images[index])
    mask_path = os.path.join(self.mask_dir, self.images[index].replace("_color.png", "_mask.png"))

    # load image and mask
    # np array because we'll use the albumentations library for 
    # data augmentation
    image = np.array(Image.open(img_path).convert("RGB"))
    # 0.0, 255.0, "L" is for grayscale in PIL library
    mask = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)
    # convert 255 to 1
    mask[mask == 255.0] = 1.0

    # if you want to apply data augmentation
    if self.transform is not None:
      augmentations = self.transform(image=image, mask=mask)
      image = augmentations["image"]
      mask = augmentations["mask"]

    return image, mask