from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from torchvision import transforms
from lenet import LeNet5
import io

app = FastAPI()

# Load model
model = LeNet5(input_channels=1, input_height=28, input_width=28, num_classes=10)
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

# Preprocessing
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(image)
            predicted = torch.argmax(output, dim=1).item()
        return {"prediction": predicted}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
