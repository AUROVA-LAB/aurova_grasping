import torch
import torch.nn as nn
import segmentation_models_pytorch as smp


class UnetPlusPlus(nn.Module):
    def __init__(self, encoder, enc_weights, in_channels, out_channels) -> None:
        super().__init__()

        self.model = smp.UnetPlusPlus(
            encoder_name=encoder,
            encoder_weights=enc_weights, 
            in_channels=in_channels,
            classes=out_channels,
        )

    def forward(self, x):
        return self.model(x)

      
class PSPNet(nn.Module):
    def __init__(self, encoder, enc_weights, in_channels, out_channels) -> None:
        super().__init__()

        self.model = smp.PSPNet(
            encoder_name=encoder,
            encoder_weights=enc_weights, 
            in_channels=in_channels,
            classes=out_channels,
        )

    def forward(self, x):
        return self.model(x)


class DeepLabV3Plus(nn.Module):
    def __init__(self, encoder, enc_weights, in_channels, out_channels) -> None:
        super().__init__()

        self.model = smp.DeepLabV3Plus(
            encoder_name=encoder,
            encoder_weights=enc_weights, 
            in_channels=in_channels,
            classes=out_channels,
        )

    def forward(self, x):
        return self.model(x)
