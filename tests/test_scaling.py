
import unittest
from unittest.mock import MagicMock, patch
import numpy as np

# Mocking modules that might not be installed in the environment
import sys
sys.modules['ultralytics'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['PIL'] = MagicMock()

# Import the function to test
# We need to add the project path to sys.path
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ml_engine')))
from vision.yolo_detector import detect_solar_area

class TestScalingAccuracy(unittest.TestCase):

    @patch('vision.yolo_detector.model')
    @patch('vision.yolo_detector.Image.open')
    def test_gsd_scaling(self, mock_open, mock_model):
        # Case 1: Provided GSD
        # Setup mock image and model results
        mock_open.return_value.convert.return_value = np.zeros((100, 100, 3))
        
        # Mock result with 1000 roof pixels
        mock_result = MagicMock()
        mock_mask = np.zeros((100, 100))
        mock_mask[:10, :10] = 1.0 # 100 pixels
        mock_result.masks.data.cpu.return_value.numpy.return_value = [mock_mask]
        mock_result.boxes.cls.cpu.return_value.numpy.return_value = [0] # 0 = roof class (anything other than 2/7)
        mock_model.return_value = [mock_result]

        # Test with GSD = 0.5 m/px. 100 pixels * (0.5*0.5) = 25 m2
        area = detect_solar_area(b"fake_bytes", gsd_m_px=0.5)
        self.assertEqual(area, 25.0)
        print(f"GSD Scaling Correct: 100 pixels @ 0.5m/px -> {area} m2")

    @patch('vision.yolo_detector.model')
    @patch('vision.yolo_detector.Image.open')
    def test_car_calibration(self, mock_open, mock_model):
        # Case 2: Reference Object Calibration (Car)
        mock_open.return_value.convert.return_value = np.zeros((100, 100, 3))
        
        # Mock results: 1 car (100 pixels) and 1 target area (500 pixels)
        mock_result = MagicMock()
        mask_car = np.zeros((100, 100))
        mask_car[0:10, 0:10] = 1.0 # 100 pixels
        
        mask_target = np.zeros((100, 100))
        mask_target[20:70, 20:30] = 1.0 # 500 pixels
        
        mock_result.masks.data.cpu.return_value.numpy.return_value = [mask_car, mask_target]
        mock_result.boxes.cls.cpu.return_value.numpy.return_value = [2, 0] # 2=car, 0=other
        mock_model.return_value = [mock_result]

        # Calibration: 100 pixels = 10m2 -> 1 pixel = 0.1m2
        # Target: 500 pixels * 0.1 = 50 m2
        area = detect_solar_area(b"fake_bytes")
        self.assertEqual(area, 50.0)
        print(f"Car Calibration Correct: 100px car/500px area -> {area} m2")

if __name__ == "__main__":
    unittest.main()
