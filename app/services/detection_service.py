import os
import pickle                                      
import numpy as np
from datetime import datetime
from flask import current_app
from detection.feature_extractor import extract_features
from detection.preprocessor import preprocess_input


class DetectionService:                                     """
    Core detection service for NIDS
    """

    def __init__(self):
        self.model = None                                       self.scaler = None
        self.encoder = None
        self._load_artifacts()

    # LOAD MODEL ARTIFACTS

    def _load_artifacts(self):
        try:
            config = current_app.config if current_app else None

            model_path = config.get("MODEL_PATH") if config else "models/model.pkl"
            scaler_path = config.get("SCALER_PATH") if config else "models/scaler.pkl"
            encoder_path = config.get("ENCODER_PATH") if config else "models/encoder.pkl"

            # Load model
            if os.path.exists(model_path):
                with open(model_path, "rb") as f:
                    self.model = pickle.load(f)
            else:
                raise FileNotFoundError("Model file not found")

            # Load scaler
            if os.path.exists(scaler_path):
                with open(scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)

            # Load encoder (optional)
            if os.path.exists(encoder_path):
                with open(encoder_path, "rb") as f:
                    self.encoder = pickle.load(f)

        except Exception as e:
            print(f"[MODEL LOAD ERROR] {str(e)}")
            self.model = None

    # PREDICTION

    def predict(self, input_data: dict) -> dict:
        """
        Perform intrusion detection
        """
        try:
            if self.model is None:
                return self._error_response("Model not loaded")

            # PREPROCESS INPUT

            processed = preprocess_input(input_data)

            # FEATURE EXTRACTION
    
            features = extract_features(processed)

            features = np.array(features).reshape(1, -1)

            # SCALING
    
            if self.scaler:
                features = self.scaler.transform(features)

            # PREDICTION
        
            prediction = self.model.predict(features)[0]

            # CONFIDENCE
        
            confidence = self._get_confidence(features)

            # LABEL DECODING
      
            attack_type = self._decode_label(prediction)

            label = "Attack" if attack_type != "Normal" else "Normal"

            return {
                "label": label,
                "attack_type": attack_type,
                "confidence": confidence,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            current_app.logger.error(f"[PREDICTION ERROR] {str(e)}")
            return self._error_response("Prediction failed")

    # CONFIDENCE SCORE
    
    def _get_confidence(self, features):
        try:
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(features)[0]
                return round(float(np.max(probs)) * 100, 2)
            return None
        except:
            return None

    # LABEL DECODER
  
    def _decode_label(self, prediction):
        try:
            if self.encoder:
                return self.encoder.inverse_transform([prediction])[0]
            return str(prediction)
        except:
            return str(prediction)

    # ERROR RESPONSE
    
    def _error_response(self, message):
        return {
            "label": "Error",
            "attack_type": "Unknown",
            "confidence": None,
            "timestamp": datetime.utcnow().isoformat(),
            "error": message
      }
