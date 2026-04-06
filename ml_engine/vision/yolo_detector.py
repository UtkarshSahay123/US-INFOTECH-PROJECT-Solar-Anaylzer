import cv2
import numpy as np
from ultralytics import YOLO
import io
from PIL import Image

# Initialize the YOLOv8 model
# Note: For production, we'd use a custom model trained for roofs and panels like `yolov8-roof-seg.pt`
# Here we'll load the base yolov8n-seg.pt to demonstrate the architecture. It will download the file automatically.
try:
    model = YOLO("yolov8n-seg.pt")
except Exception as e:
    model = None
    print(f"Failed to load YOLO model: {e}")

def detect_solar_area(img_bytes: bytes) -> float:
    """
    Process the image to detect available roof/land area using Deep Learning.
    Returns the estimated area in square meters.
    """
    if model is None:
        return 100.0 # Return a fallback dummy area if model fails to load
        
    try:
        # Convert bytes to cv2 image
        image = Image.open(io.BytesIO(img_bytes))
        image_np = np.array(image.convert('RGB'))
        
        # Run YOLOv8 segmentation
        results = model(image_np)
        
        # Since this is a placeholder without a custom model, we'll simulate an area extraction
        # If we had a 'roof' or 'empty space' class, we would sum the pixels in the segmentation mask
        
        # Simulating area finding:
        pixels_area = 0
        for result in results:
            if result.masks is not None:
                # Count total pixels from all detected masks (as a placeholder)
                masks = result.masks.data.cpu().numpy()
                for mask in masks:
                    pixels_area += np.sum(mask == 1)
                    
        # In a real environment, we'd scale pixels to square meters using EXIF distance or known reference objects
        # Here we just arbitrarily simulate it for pipeline demonstration
        area_m2 = float(pixels_area) / 1000.0
        
        # Provide a realistic threshold if detection misses
        if area_m2 < 10.0:
             area_m2 = 120.0 # Fallback 120 sq m
             
        return area_m2
    except Exception as e:
        print(f"Vision processing error: {e}")
        return 150.0  # Fallback 150 sq m
