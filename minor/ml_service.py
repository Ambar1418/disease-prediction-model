import os
import sys
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from keras_self_attention import SeqSelfAttention
from keras_multi_head import MultiHeadAttention

class MLModelService:
    """Service class to handle ML model operations for Django integration"""
    
    def __init__(self):
        self.model = None
        self.class_names = [
            'Alopecia Areata',
            'Contact Dermatitis', 
            'Folliculitis',
            'Head Lice',
            'Lichen Planus',
            'Male Pattern Baldness',
            'Psoriasis',
            'Seborrheic Dermatitis',
            'Telogen Effluvium',
            'Tinea Capitis'
        ]
        self.load_model()
    
    def load_model(self):
        """Load the trained model with custom objects"""
        try:
            # Get the path to the model file (assuming it's in the parent directory)
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hair-diseases.h5')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            
            self.model = load_model(
                model_path,
                custom_objects={
                    "SeqSelfAttention": SeqSelfAttention,
                    "MultiHeadAttention": MultiHeadAttention
                }
            )
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            self.model = None
    
    def preprocess_image(self, img: Image.Image):
        """Preprocess image for model prediction"""
        try:
            img = img.resize((128, 128))  # Match model's input size
            img_array = np.array(img) / 255.0
            return np.expand_dims(img_array, axis=0)
        except Exception as e:
            print(f"❌ Error preprocessing image: {str(e)}")
            return None
    
    def predict(self, image_file):
        """Make prediction on uploaded image"""
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Open and convert image
            img = Image.open(image_file).convert("RGB")
            
            # Preprocess image
            processed = self.preprocess_image(img)
            if processed is None:
                return {"error": "Failed to preprocess image"}
            
            # Make prediction
            prediction = self.model.predict(processed)
            predicted_class = self.class_names[np.argmax(prediction)]
            confidence = float(np.max(prediction))
            
            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "success": True
            }
        except Exception as e:
            print(f"❌ Error during prediction: {str(e)}")
            return {"error": f"Prediction failed: {str(e)}"}

# Global instance - lazy loading to avoid startup crashes
_ml_service_instance = None

def get_ml_service():
    """Get or create ML service instance (lazy loading)"""
    global _ml_service_instance
    if _ml_service_instance is None:
        try:
            _ml_service_instance = MLModelService()
        except Exception as e:
            print(f"❌ Failed to initialize ML service: {str(e)}")
            # Return a dummy service that will fail gracefully
            class DummyMLService:
                def predict(self, image_input):
                    return {"error": "Model not available", "success": False}
            _ml_service_instance = DummyMLService()
    return _ml_service_instance
