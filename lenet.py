import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch import Tensor

class LeNet5(nn.Module):
    def __init__(self, input_channels: int, input_height: int, input_width: int, num_classes: int) -> None:
        super(LeNet5, self).__init__()

        # First convolutional layer
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=input_channels, out_channels=6, kernel_size=5, stride=1, padding='same'),
            nn.BatchNorm2d(6),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        # Second convolutional layer
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1, padding='same'),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        # Compute the flattened size
        with torch.no_grad():
            sample_input = torch.randn(1, input_channels, input_height, input_width)
            sample_output = self.layer2(self.layer1(sample_input))
            flattened_size = sample_output.view(1, -1).shape[1]
        
        self.fc = nn.Linear(flattened_size,120)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(120,84)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(84, num_classes)

    def forward(self, x: Tensor) -> Tensor:
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1) # flatten cnn features to fit to the fully connected layer
        out = self.fc(out)
        out = self.relu(out)
        out = self.fc1(out)
        out = self.relu1(out)
        out = self.fc2(out)
        return out