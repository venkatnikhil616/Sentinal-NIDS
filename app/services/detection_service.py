import os

from detection.detector import Detector
from detection.feature_extractor import extract_features
from detection.preprocessor import preprocess


class DetectionService:
    def __init__(self):
        # ✅ FIX: pass model path
        model_path = os.path.join("models", "model.pkl")

        # If your Detector supports more files, add them here
        self.detector = Detector(model_path)

    def detect(self, raw_data: dict):
        try:
            # Extract features
            features = extract_features(raw_data)

            # Preprocess
            processed = preprocess(features)

            # Predict
            prediction, confidence = self.detector.predict(processed)

            return {
                "prediction": prediction,
                "confidence": confidence
            }

        except Exception as e:
            return {
                "error": str(e)
            }
