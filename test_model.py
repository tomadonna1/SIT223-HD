import os
import torch
from PIL import Image
from torchvision import transforms
from lenet import LeNet5

# Load model
model = LeNet5(input_channels=1, input_height=28, input_width=28, num_classes=10)
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def predict_image(image_path):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0) 
    with torch.no_grad():
        output = model(image)
    predicted_class = torch.argmax(output, dim=1).item()
    return predicted_class

def main():
    test_dir = os.path.join(os.path.dirname(__file__), "test_images")
    for filename in os.listdir(test_dir):
        if filename.endswith(".png"):
            path = os.path.join(test_dir, filename)
            prediction = predict_image(path)
            print(f"{filename} → Prediction: {prediction}")

if __name__ == "__main__":
    main()
