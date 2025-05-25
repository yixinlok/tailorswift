from torch import nn
from torchvision import models

def get_resnet_model(freeze, num_attributes):
    model = models.resnet18()
    for param in model.parameters():
        param.requires_grad = freeze

    n_inputs = model.fc.in_features

    model.fc = nn.Sequential(
        nn.Linear(n_inputs, num_attributes, bias=True),
        nn.Sigmoid() # Restrict to (0,1)
    )

    model.conv_1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2))

    model = model.to('cuda')
    return model

def get_vit_model(freeze, num_attributes):
    model = models.vit_b_16(weights='DEFAULT')

    for param in model.parameters():
        param.requires_grad = freeze

    n_inputs = model.heads.head.in_features
    model.heads = nn.Sequential(
        nn.Linear(n_inputs, num_attributes, bias=True),
        nn.Sigmoid() # Restrict to (0,1)
    )

    model.conv_proj = nn.Conv2d(1, 768, kernel_size=(16, 16), stride=(16, 16))
    model = model.to('cuda')
    return model