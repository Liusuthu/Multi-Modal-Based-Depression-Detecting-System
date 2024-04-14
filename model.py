"""
File: model.py
Author: Elena Ryumina and Dmitry Ryumin
Description: This module provides functions for loading and processing a pre-trained deep learning model
             for facial expression recognition.
License: MIT License
"""

import torch
import requests
from PIL import Image
from torchvision import transforms
from pytorch_grad_cam import GradCAM

# Importing necessary components for the Gradio app
from config import config_data
from model_architectures import ResNet50, LSTMPyTorch


def load_model(model_url, model_path):
    try:
        with requests.get(model_url, stream=True) as response:
            with open(model_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        return model_path
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

path_static = load_model(config_data.model_static_url, config_data.model_static_path)   
pth_model_static = ResNet50(7, channels=3)
pth_model_static.load_state_dict(torch.load(path_static))
pth_model_static.eval()

path_dynamic = load_model(config_data.model_dynamic_url, config_data.model_dynamic_path) 
pth_model_dynamic = LSTMPyTorch()
pth_model_dynamic.load_state_dict(torch.load(path_dynamic))
pth_model_dynamic.eval()

target_layers = [pth_model_static.layer4]
cam = GradCAM(model=pth_model_static, target_layers=target_layers)

def pth_processing(fp):
    class PreprocessInput(torch.nn.Module):
        def init(self):
            super(PreprocessInput, self).init()

        def forward(self, x):
            x = x.to(torch.float32)
            x = torch.flip(x, dims=(0,))
            x[0, :, :] -= 91.4953
            x[1, :, :] -= 103.8827
            x[2, :, :] -= 131.0912
            return x

    def get_img_torch(img, target_size=(224, 224)):
        transform = transforms.Compose([transforms.PILToTensor(), PreprocessInput()])
        img = img.resize(target_size, Image.Resampling.NEAREST)
        img = transform(img)
        img = torch.unsqueeze(img, 0)
        return img

    return get_img_torch(fp)
