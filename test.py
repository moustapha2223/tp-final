from ultralytics import YOLO
from PIL import Image

# Load the model
model = YOLO("yolov8n.yaml")  # Make sure the model path is correct

# Specify the path to the test image
image_path = "C:/Users/mousa/Downloads/orchestration ML/bus.jpg"

# Load the image using PIL (Pillow)
img = Image.open(image_path)

# Perform prediction on the image
results = model(img)

# Access the prediction data
#predictions = results

# Print the predictions
print(results)

#results.show()


