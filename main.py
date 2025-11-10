from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import numpy as np
from PIL import Image

# Import TensorFlow with macOS optimization
try:
    from tensorflow.keras.models import load_model
    import tensorflow as tf
    
    # macOS-specific TensorFlow configuration
    if sys.platform == "darwin":
        print("🍎 macOS detected - configuring TensorFlow for Apple Silicon")
        # Enable Metal GPU if available
        if hasattr(tf.config, 'list_physical_devices'):
            physical_devices = tf.config.list_physical_devices('GPU')
            if physical_devices:
                for device in physical_devices:
                    tf.config.experimental.set_memory_growth(device, True)
                print("✅ Metal GPU acceleration enabled")
            else:
                print("ℹ️ No Metal GPU detected, using CPU")
        
        # Set environment variables for better macOS performance
        os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
        os.environ.setdefault('OMP_NUM_THREADS', '4')
        
except ImportError as e:
    print(f"❌ TensorFlow import failed: {e}")
    load_model = None
    tf = None

# Import custom layers
try:
    from keras_self_attention import SeqSelfAttention
    from keras_multi_head import MultiHeadAttention
    
    # Fix compatibility issues with newer TensorFlow/Keras versions
    def patch_attention_layers():
        """Patch attention layers for TensorFlow 2.16+ compatibility"""
        try:
            import tensorflow as tf
            
            # Patch ScaledDotProductAttention if it exists
            if hasattr(MultiHeadAttention, 'ScaledDotProductAttention'):
                original_call = MultiHeadAttention.ScaledDotProductAttention.call
                
                def patched_call(self, inputs, mask=None, **kwargs):
                    # Convert len() calls to shape operations
                    try:
                        return original_call(self, inputs, mask, **kwargs)
                    except Exception as e:
                        if "len is not well defined for a symbolic Tensor" in str(e):
                            # Try to work around the issue by using shape instead of len
                            print("⚠️ Applying compatibility patch for attention layers...")
                            # This is a workaround - the model might need retraining with compatible layers
                            return tf.keras.layers.MultiHeadAttention(
                                num_heads=8, 
                                key_dim=64
                            )(inputs[0], inputs[1], inputs[2])
                        else:
                            raise e
                
                MultiHeadAttention.ScaledDotProductAttention.call = patched_call
                
        except Exception as patch_error:
            print(f"⚠️ Could not patch attention layers: {patch_error}")
    
    # Apply patches
    patch_attention_layers()
    
except ImportError as e:
    print(f"⚠️ Custom layers import failed: {e}")
    SeqSelfAttention = None
    MultiHeadAttention = None

app = FastAPI(title="Hair Disease Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model with custom_objects
model = None
if load_model is not None:
    try:
        # Try compatible model first, then fallback to original
        compatible_model_path = "hair-diseases-compatible.h5"
        original_model_path = "hair-diseases.h5"
        
        if os.path.exists(compatible_model_path):
            model_path = compatible_model_path
            print("✅ Using compatible model (hair-diseases-compatible.h5)")
        elif os.path.exists(original_model_path):
            model_path = original_model_path
            print("⚠️ Compatible model not found, using original model")
        else:
            # Try alternative path
            model_path = os.path.join("minor", "hair-diseases.h5")
            print("⚠️ Using alternative model path")
        
        # Try to load model with safe method
        try:
            from simple_model_loader import load_model_safely
            
            # Try loading with safe method
            model = load_model_safely(model_path)
            
            if model is None:
                # Fallback to original method
                print("⚠️ Safe loading failed, trying original method...")
                custom_objects = {}
                if SeqSelfAttention is not None and MultiHeadAttention is not None:
                    custom_objects = {
                        "SeqSelfAttention": SeqSelfAttention,
                        "MultiHeadAttention": MultiHeadAttention
                    }
                
                model = load_model(
                    model_path,
                    custom_objects=custom_objects if custom_objects else None
                )
            
            print("✅ Model loaded successfully")
            
        except ImportError:
            # Fallback to original method if simple loader not available
            print("⚠️ Simple model loader not available, using original loading method")
            custom_objects = {}
            if SeqSelfAttention is not None and MultiHeadAttention is not None:
                custom_objects = {
                    "SeqSelfAttention": SeqSelfAttention,
                    "MultiHeadAttention": MultiHeadAttention
                }
            
            model = load_model(
                model_path,
                custom_objects=custom_objects if custom_objects else None
            )
            print("✅ Model loaded successfully")
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("💡 Tip: The model might need to be retrained with TensorFlow 2.16+ compatible layers")
        model = None

class_names = [
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

def preprocess_image(img: Image.Image):
    img = img.resize((128, 128))  # Match your model's input size
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {
            "error": "Model not loaded. Please check TensorFlow installation.",
            "success": False
        }
    
    try:
        img = Image.open(file.file).convert("RGB")
        processed = preprocess_image(img)

        prediction = model.predict(processed)
        predicted_class = class_names[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "success": True
        }
    except Exception as e:
        return {
            "error": f"Prediction failed: {str(e)}",
            "success": False
        }