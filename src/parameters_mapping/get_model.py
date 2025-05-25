import torch
from torchvision import models
from torch import nn
from torchvision.io import read_image
from torchvision import transforms
import numpy as np
import os

def get_vit(file_path, num_attributes):
    model = models.vit_b_16(weights='DEFAULT')

    n_inputs = model.heads.head.in_features
    model.heads = nn.Sequential(
        nn.Linear(n_inputs, num_attributes, bias=True),
        nn.Sigmoid() # Restrict to (0,1)
        # ClippedReLU()   
    )

    
    model.conv_proj = nn.Conv2d(1, 768, kernel_size=(16, 16), stride=(16, 16))
    device = torch.device("cpu")  # Ensure it's set to CPU

    if os.path.exists(file_path):
        model.load_state_dict(torch.load(file_path,  map_location=device))
    else:
        print("File doesn't exist")
    model.to(device)
    model.eval() 
    return model


transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ColorJitter(brightness=0.3, contrast=0.5, saturation=0.3, hue=0.3),
        transforms.Grayscale(num_output_channels=1),
        transforms.GaussianBlur(kernel_size=5, sigma=(0.1, 2.0)),
        # transforms.Normalize([0.485, 0.456, 0.406],
        #                      [0.229, 0.224, 0.225])  # Imagenet standards
    ])

def test_model(model, image_path):
    image = read_image(image_path)
    image = image.type(torch.FloatTensor)/ 255.0
    image = transform(image).unsqueeze(0)
    print(image.shape)
    out = model(image)
    out = out.squeeze(0)
    return out
