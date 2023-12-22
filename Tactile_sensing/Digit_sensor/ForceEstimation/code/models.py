import torch
import torch.nn as nn
from torchvision import models
from torchsummary import summary

from torchvision.models.resnet import BasicBlock

class Resnet_modified(models.ResNet):
    def __init__(self) -> None:
        super().__init__(BasicBlock, [2,2,2,2])
        self.fc1 = nn.Linear(128, 512)
        self.fc2 = nn.Linear(256, 512)
        self.fc3 = nn.Linear(512, 1)
        self.fc4 = nn.Linear(1536, 1)

        
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)

        out1 = self.avgpool(x)
        out1 = torch.flatten(out1, 1)
        out1 = self.fc1(out1)
        
        x = self.layer3(x)

        out2 = self.avgpool(x)
        out2 = torch.flatten(out2, 1)
        out2 = self.fc2(out2)
        
        x = self.layer4(x)

        out3 = self.avgpool(x)
        out3 = torch.flatten(out3, 1)
        #out3 = self.fc3(out3)

        x = torch.cat((out1, out2, out3), dim=1)

        x = self.fc4(x)
        
        return x


class ImageToForce(nn.Module):
    def __init__(self, enc_weights=None) -> None:
        super().__init__()

        self.model = models.resnet18(weights=enc_weights)
        # last layer for a regression problem is a linear layer
        # same in features as in original resnet18 model, but we 
        # need to change the output to only one value (regression of force value)
        self.model.fc = nn.Linear(self.model.fc.in_features, 1)
        summary(self.model, (3, 320, 240), device="cpu")
        
        
    def forward(self, x):
        return self.model(x)



class DepthImageToForce(nn.Module):
    def __init__(self, encoder=None, enc_weights=None, in_channels=None, out_channels=None) -> None:
        super().__init__()

        self.model = models.resnet18(weights=enc_weights)
        # last layer for a regression problem is a linear layer
        # same in features as in original resnet18 model, but we 
        # need to change the output to only one value (regression of force value)
        self.model.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = nn.Linear(self.model.fc.in_features, 1)
        summary(self.model, (1, 320, 240), device="cpu")
        
    
        
    def forward(self, x):
        return self.model(x)


class RGBDToForce(nn.Module):
    def __init__(self, encoder=None, enc_weights=None, in_channels=None, out_channels=None) -> None:
        super().__init__()

        self.model = models.resnet18(weights=enc_weights)
        # last layer for a regression problem is a linear layer
        # same in features as in original resnet18 model, but we 
        # need to change the output to only one value (regression of force value)
        self.model.conv1 = nn.Conv2d(4, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = nn.Linear(self.model.fc.in_features, 1)
        summary(self.model, (4, 320, 240), device="cpu")
        
    
        
    def forward(self, x):
        return self.model(x)
    



class RGBandDToForce(nn.Module):
    def __init__(self, encoder=None, enc_weights=None, in_channels=None, out_channels=None) -> None:
        super().__init__()

        self.model_rgb = models.resnet18(weights=enc_weights)
        self.model_mask = models.resnet18(weights=enc_weights)
        # last layer for a regression problem is a linear layer
        # same in features as in original resnet18 model, but we 
        # need to change the output to only one value (regression of force value)
        
        self.rgb_before_fc = list(self.model_rgb.children())[:-1]  # children returns all layers, [:-1] -> 
        # all layers except last one (fc)
        self.model_rgb_before_fc = nn.Sequential(*self.rgb_before_fc)
        
        self.model_mask.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.mask_before_fc = list(self.model_mask.children())[:-1]  # children returns all layers, [:-1] -> 
        # all layers except last one (fc)
        self.model_mask_before_fc = nn.Sequential(*self.mask_before_fc)
        #summary(self.model_rgb_before_fc, (3, 320, 240), device="cpu")
        #summary(self.model_mask_before_fc, (1, 320, 240), device="cpu")
        
        self.fc1 = nn.Linear(1024, 16)  # resnet18 outputs batchsize x 512 x 1 x 1
        # after contatenating both feature maps from the two diff resnets and using a 
        # batchsize of 16, we have 16 x 1024 x 1 x 1
        # To multiply the matrices inside the nn.Linear layer, mxn * nxp and the output
        # is of dim mxp. Then, we define a linear layer with dim 1024x16, which output
        # is of dim 16x16. Finally, we define another linear layer with 16 neurons as input
        # and only one layer to estimate the force value.
        self.fc2 = nn.Linear(16, 1)
    
        
    def forward(self, rgb, mask):

        y1 = self.model_rgb_before_fc(rgb)
        y2 = self.model_mask_before_fc(mask)

        y1 = y1.view(-1, y1.size(1))
        y2 = y2.view(-1, y2.size(1))

        y3_concat = torch.cat((y1, y2), dim=1)

        return self.fc2(self.fc1(y3_concat))
