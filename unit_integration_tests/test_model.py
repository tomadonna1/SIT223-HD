import os
import sys
import torch
from PIL import Image
from torchvision import transforms
import pytest

# Add parent directory to sys.path so lenet.py can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lenet import LeNet5 

# Load model once for all tests
@pytest.fixture(scope="module")
def model():
    model = LeNet5(input_channels=1, input_height=28, input_width=28, num_classes=10)
    model.load_state_dict(torch.load("model.pth", map_location="cpu"))
    model.eval()
    return model

# Transformation pipeline
@pytest.fixture(scope="module")
def transform():
    return transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

# Get test images
def get_test_images():
    test_dir = os.path.join(os.path.dirname(__file__), "..", "test_images")
    return [
        os.path.join(test_dir, fname)
        for fname in os.listdir(test_dir)
        if fname.endswith(".png")
    ]

# Test predictions
@pytest.mark.parametrize("image_path", get_test_images())
def test_prediction(model, transform, image_path):
    image = Image.open(image_path)
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
    predicted = torch.argmax(output, dim=1).item()
    
    # Just check it's a valid class (0–9)
    assert 0 <= predicted <= 9, f"Invalid prediction {predicted} for {image_path}"
