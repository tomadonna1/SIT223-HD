import requests

def test_predict():
    image_path = "test_images/3.png"  
    url = "http://localhost:8000/predict"

    with open(image_path, "rb") as f:
        response = requests.post(url, files={"file": f})

    assert response.status_code == 200, f"Request failed: {response.text}"
    json_data = response.json()
    assert "prediction" in json_data, "No 'prediction' field in response"
    print("Integration test passed! Prediction:", json_data["prediction"])

if __name__ == "__main__":
    test_predict()
