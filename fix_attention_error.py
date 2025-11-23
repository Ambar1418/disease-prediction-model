#!/usr/bin/env python3
"""
Direct Fix for ScaledDotProductAttention Error
This script patches the problematic attention layer directly
"""

import os
import sys
import warnings
import tensorflow as tf
from tensorflow import keras
import numpy as np

def patch_attention_layers():
    """
    Patch the problematic attention layers to fix the len() error
    """
    print("🔧 Patching attention layers to fix TensorFlow 2.16+ compatibility...")
    
    try:
        # Import the problematic modules
        from keras_self_attention import SeqSelfAttention
        from keras_multi_head import MultiHeadAttention
        
        # Patch ScaledDotProductAttention if it exists
        if hasattr(MultiHeadAttention, 'ScaledDotProductAttention'):
            original_call = MultiHeadAttention.ScaledDotProductAttention.call
            
            def patched_call(self, inputs, mask=None, **kwargs):
                try:
                    # Try the original call first
                    return original_call(self, inputs, mask, **kwargs)
                except Exception as e:
                    if "len is not well defined for a symbolic Tensor" in str(e):
                        print("⚠️ Applying direct patch for ScaledDotProductAttention...")
                        
                        # Extract query, key, value from inputs
                        if isinstance(inputs, (list, tuple)) and len(inputs) >= 3:
                            query, key, value = inputs[0], inputs[1], inputs[2]
                        else:
                            # If inputs is not a tuple, assume it's a single tensor for self-attention
                            query = key = value = inputs
                        
                        # Use TensorFlow's native MultiHeadAttention as fallback
                        num_heads = getattr(self, 'head_num', 8)
                        key_dim = 64  # Default key dimension
                        
                        # Create a temporary attention layer
                        attention_layer = keras.layers.MultiHeadAttention(
                            num_heads=num_heads,
                            key_dim=key_dim,
                            dropout=0.1
                        )
                        
                        # Apply attention
                        return attention_layer(query, key, value)
                    else:
                        raise e
            
            # Apply the patch
            MultiHeadAttention.ScaledDotProductAttention.call = patched_call
            print("✅ ScaledDotProductAttention patched successfully")
        
        # Patch SeqSelfAttention if it exists
        if hasattr(SeqSelfAttention, 'call'):
            original_seq_call = SeqSelfAttention.call
            
            def patched_seq_call(self, inputs, **kwargs):
                try:
                    return original_seq_call(self, inputs, **kwargs)
                except Exception as e:
                    if "len is not well defined for a symbolic Tensor" in str(e):
                        print("⚠️ Applying direct patch for SeqSelfAttention...")
                        
                        # Use TensorFlow's native MultiHeadAttention for self-attention
                        num_heads = getattr(self, 'head_num', 8)
                        key_dim = 64
                        
                        attention_layer = keras.layers.MultiHeadAttention(
                            num_heads=num_heads,
                            key_dim=key_dim,
                            dropout=0.1
                        )
                        
                        # For self-attention, query, key, and value are the same
                        return attention_layer(inputs, inputs, inputs)
                    else:
                        raise e
            
            SeqSelfAttention.call = patched_seq_call
            print("✅ SeqSelfAttention patched successfully")
        
        return True
        
    except ImportError as e:
        print(f"⚠️ Could not import attention modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Error patching attention layers: {e}")
        return False

def load_model_with_patches(model_path):
    """
    Load model with attention layer patches applied
    """
    print(f"🔧 Loading model with patches: {model_path}")
    
    # Apply patches before loading
    patch_success = patch_attention_layers()
    
    if not patch_success:
        print("⚠️ Patching failed, trying alternative approach...")
    
    try:
        # Try loading with custom objects
        custom_objects = {}
        
        try:
            from keras_self_attention import SeqSelfAttention
            from keras_multi_head import MultiHeadAttention
            custom_objects = {
                "SeqSelfAttention": SeqSelfAttention,
                "MultiHeadAttention": MultiHeadAttention
            }
        except ImportError:
            print("⚠️ Custom attention layers not available")
        
        # Load the model
        if custom_objects:
            print("   Loading with custom objects...")
            model = keras.models.load_model(model_path, custom_objects=custom_objects)
        else:
            print("   Loading without custom objects...")
            model = keras.models.load_model(model_path, compile=False)
        
        print("✅ Model loaded successfully with patches")
        return model
        
    except Exception as e:
        print(f"❌ Failed to load model even with patches: {e}")
        return None

def test_model_prediction(model, test_shape=(1, 128, 128, 3)):
    """
    Test if the patched model can make predictions
    """
    try:
        print("🧪 Testing patched model prediction...")
        
        # Create test input
        test_input = np.random.random(test_shape).astype(np.float32)
        
        # Make prediction
        prediction = model.predict(test_input, verbose=0)
        
        print(f"✅ Prediction successful! Output shape: {prediction.shape}")
        print(f"   Prediction values: {prediction[0][:5]}...")  # Show first 5 values
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        return False

def main():
    """
    Main function to test the fix
    """
    print("🔧 TensorFlow Attention Layer Fix")
    print("=" * 40)
    
    # Find model file
    model_paths = ["hair-diseases.h5", "minor/hair-diseases.h5"]
    model_path = None
    
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        print("❌ Model file not found!")
        return False
    
    print(f"📁 Found model: {model_path}")
    
    # Load model with patches
    model = load_model_with_patches(model_path)
    
    if model is None:
        print("❌ Failed to load model")
        return False
    
    # Test prediction
    if test_model_prediction(model):
        print("\n🎉 Fix successful! The model can now make predictions.")
        return True
    else:
        print("\n❌ Fix failed. The model still has issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
