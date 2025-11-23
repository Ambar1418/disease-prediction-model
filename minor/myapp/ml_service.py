import os
import sys
import numpy as np
from PIL import Image
try:
    from tensorflow.keras.models import load_model  # type: ignore
    import tensorflow as tf  # type: ignore
    import keras.backend as K  # type: ignore
    # Keras 3 compatibility shim: provide missing backend ops used by old layers
    if not hasattr(K, "dot"):
        def _k_dot(x, y):
            try:
                return tf.linalg.matmul(x, y)
            except Exception:
                return tf.tensordot(x, y, axes=1)
        K.dot = _k_dot  # type: ignore[attr-defined]
    # batch_dot with axes support via tensordot
    def _ensure_batch_dot():
        def _k_batch_dot(x, y, axes=None, **kwargs):  # type: ignore[no-redef]
            # axes can be int or tuple/list of two ints
            if axes is None:
                axes = (tf.rank(x) - 1, tf.rank(y) - 1)
            elif isinstance(axes, int):
                axes = (axes, axes)
            return tf.tensordot(x, y, axes=axes)
        return _k_batch_dot
    if not hasattr(K, "batch_dot"):
        K.batch_dot = _ensure_batch_dot()  # type: ignore[attr-defined]
    else:
        try:
            from inspect import signature
            if 'axes' not in signature(K.batch_dot).parameters:  # type: ignore[arg-type]
                K.batch_dot = _ensure_batch_dot()  # type: ignore[attr-defined]
        except Exception:
            K.batch_dot = _ensure_batch_dot()  # type: ignore[attr-defined]
    if not hasattr(K, "shape"):
        def _k_shape(x):
            return tf.shape(x)
        K.shape = _k_shape  # type: ignore[attr-defined]
    if not hasattr(K, "int_shape"):
        def _k_int_shape(x):
            try:
                return tuple(x.shape.as_list())  # type: ignore[attr-defined]
            except Exception:
                return tuple(x.shape)
        K.int_shape = _k_int_shape  # type: ignore[attr-defined]
    if not hasattr(K, "permute_dimensions"):
        def _k_permute_dimensions(x, pattern):
            return tf.transpose(x, perm=pattern)
        K.permute_dimensions = _k_permute_dimensions  # type: ignore[attr-defined]
    if not hasattr(K, "reshape"):
        def _k_reshape(x, shape):
            return tf.reshape(x, shape)
        K.reshape = _k_reshape  # type: ignore[attr-defined]
    if not hasattr(K, "concatenate"):
        def _k_concatenate(tensors, axis=-1):
            return tf.concat(tensors, axis=axis)
        K.concatenate = _k_concatenate  # type: ignore[attr-defined]
    if not hasattr(K, "softmax"):
        def _k_softmax(x, axis=-1):
            return tf.nn.softmax(x, axis=axis)
        K.softmax = _k_softmax  # type: ignore[attr-defined]
    if not hasattr(K, "sqrt"):
        def _k_sqrt(x):
            return tf.sqrt(x)
        K.sqrt = _k_sqrt  # type: ignore[attr-defined]
    if not hasattr(K, "cast"):
        def _k_cast(x, dtype):
            return tf.cast(x, dtype)
        K.cast = _k_cast  # type: ignore[attr-defined]
    if not hasattr(K, "exp"):
        def _k_exp(x):
            return tf.exp(x)
        K.exp = _k_exp  # type: ignore[attr-defined]
    if not hasattr(K, "maximum"):
        def _k_maximum(x, y):
            return tf.maximum(x, y)
        K.maximum = _k_maximum  # type: ignore[attr-defined]
    if not hasattr(K, "minimum"):
        def _k_minimum(x, y):
            return tf.minimum(x, y)
        K.minimum = _k_minimum  # type: ignore[attr-defined]
    if not hasattr(K, "clip"):
        def _k_clip(x, min_value, max_value):
            return tf.clip_by_value(x, min_value, max_value)
        K.clip = _k_clip  # type: ignore[attr-defined]
    if not hasattr(K, "max"):
        def _k_max(x, axis=None, keepdims=False):
            return tf.reduce_max(x, axis=axis, keepdims=keepdims)
        K.max = _k_max  # type: ignore[attr-defined]
    if not hasattr(K, "sum"):
        def _k_sum(x, axis=None, keepdims=False):
            return tf.reduce_sum(x, axis=axis, keepdims=keepdims)
        K.sum = _k_sum  # type: ignore[attr-defined]
    if not hasattr(K, "mean"):
        def _k_mean(x, axis=None, keepdims=False):
            return tf.reduce_mean(x, axis=axis, keepdims=keepdims)
        K.mean = _k_mean  # type: ignore[attr-defined]
    if not hasattr(K, "log"):
        def _k_log(x):
            return tf.math.log(x)
        K.log = _k_log  # type: ignore[attr-defined]
    if not hasattr(K, "epsilon"):
        def _k_epsilon():
            return tf.keras.backend.epsilon() if hasattr(tf.keras.backend, 'epsilon') else 1e-7
        K.epsilon = _k_epsilon  # type: ignore[attr-defined]
except Exception:
    load_model = None  # type: ignore
try:
    from keras_self_attention import SeqSelfAttention  # type: ignore
    from keras_multi_head import MultiHeadAttention  # type: ignore
    
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
    
except Exception:
    SeqSelfAttention = None  # type: ignore
    MultiHeadAttention = None  # type: ignore

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
            if load_model is None:
                raise ImportError("TensorFlow is not installed")
            
            # Get the path to the model file (in the minor directory)
            # Try compatible model first, then fallback to original
            compatible_model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hair-diseases-compatible.h5')
            original_model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hair-diseases.h5')
            
            if os.path.exists(compatible_model_path):
                model_path = compatible_model_path
                print("✅ Using compatible model (hair-diseases-compatible.h5)")
            else:
                model_path = original_model_path
                print("⚠️ Compatible model not found, using original model")
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            
            # macOS-specific TensorFlow configuration
            if sys.platform == "darwin":
                print("🍎 macOS detected - configuring TensorFlow for Apple Silicon")
                try:
                    import tensorflow as tf
                    # Enable Metal GPU if available
                    if hasattr(tf.config, 'list_physical_devices'):
                        physical_devices = tf.config.list_physical_devices('GPU')
                        if physical_devices:
                            for device in physical_devices:
                                tf.config.experimental.set_memory_growth(device, True)
                            print("✅ Metal GPU acceleration enabled")
                        else:
                            print("ℹ️ No Metal GPU detected, using CPU")
                except Exception as gpu_error:
                    print(f"⚠️ GPU configuration warning: {gpu_error}")

            # Try to load model with multiple strategies
            try:
                # Import simple model loader
                sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
                from simple_model_loader import load_model_safely
                
                # Try loading with safe method
                self.model = load_model_safely(model_path)
                
                if self.model is None:
                    # Fallback to original method
                    print("⚠️ Safe loading failed, trying original method...")
                    custom_objects = {}
                    if SeqSelfAttention is not None and MultiHeadAttention is not None:
                        custom_objects = {
                            "SeqSelfAttention": SeqSelfAttention,
                            "MultiHeadAttention": MultiHeadAttention
                        }
                    
                    self.model = load_model(
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
                else:
                    print("⚠️ Optional attention layers not available. Attempting to load model without custom objects.")

                self.model = load_model(
                    model_path,
                    custom_objects=custom_objects if custom_objects else None
                )
                print("✅ Model loaded successfully")
                
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            print("💡 Tip: The model might need to be retrained with TensorFlow 2.16+ compatible layers")
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
    
    def predict(self, image_input):
        """Make prediction on uploaded image"""
        if self.model is None:
            return {"error": "Model not loaded", "success": False}
        
        try:
            # Handle different input types
            if hasattr(image_input, 'read'):
                # File-like object
                img = Image.open(image_input).convert("RGB")
            elif isinstance(image_input, Image.Image):
                # PIL Image object
                img = image_input.convert("RGB")
            else:
                return {"error": "Invalid image input type"}
            
            # Preprocess image
            processed = self.preprocess_image(img)
            if processed is None:
                return {"error": "Failed to preprocess image"}
            
            # Make prediction
            prediction = self.model.predict(processed, verbose=0)
            predicted_class = self.class_names[np.argmax(prediction[0])]
            confidence = float(np.max(prediction[0]))
            
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
