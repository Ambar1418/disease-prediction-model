#!/usr/bin/env python3
"""
Model Compatibility Module for Hair Disease Prediction
Handles compatibility issues between TensorFlow 2.16+ and older custom attention layers
"""

import os
import sys
import warnings
import tensorflow as tf
from tensorflow import keras

def create_compatible_attention_layer():
    """
    Create a compatible attention layer that works with TensorFlow 2.16+
    This replaces the problematic custom attention layers
    """
    try:
        # Use native TensorFlow MultiHeadAttention
        return keras.layers.MultiHeadAttention(
            num_heads=8,
            key_dim=64,
            dropout=0.1,
            name="compatible_attention"
        )
    except Exception as e:
        print(f"⚠️ Could not create compatible attention layer: {e}")
        return None

def create_compatible_self_attention_layer():
    """
    Create a compatible self-attention layer
    """
    try:
        # Use native TensorFlow MultiHeadAttention for self-attention
        return keras.layers.MultiHeadAttention(
            num_heads=8,
            key_dim=64,
            dropout=0.1,
            name="compatible_self_attention"
        )
    except Exception as e:
        print(f"⚠️ Could not create compatible self-attention layer: {e}")
        return None

def load_model_with_compatibility_fixes(model_path, custom_objects=None):
    """
    Load model with compatibility fixes for TensorFlow 2.16+
    """
    print("🔧 Loading model with compatibility fixes...")
    
    # Suppress warnings during model loading
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        try:
            # First, try to load with original custom objects
            if custom_objects:
                print("   Attempting to load with original custom objects...")
                model = keras.models.load_model(model_path, custom_objects=custom_objects)
                print("✅ Model loaded with original custom objects")
                return model
        except Exception as e:
            print(f"⚠️ Failed to load with original custom objects: {e}")
            
        try:
            # Try to load without custom objects (might work if layers are not used)
            print("   Attempting to load without custom objects...")
            model = keras.models.load_model(model_path, compile=False)
            print("✅ Model loaded without custom objects")
            return model
        except Exception as e:
            print(f"⚠️ Failed to load without custom objects: {e}")
            
        try:
            # Create compatibility mapping
            print("   Attempting to load with compatibility mapping...")
            compatibility_objects = {}
            
            # Map problematic layers to compatible ones
            if 'SeqSelfAttention' in str(e) or 'MultiHeadAttention' in str(e):
                compatibility_objects['SeqSelfAttention'] = create_compatible_self_attention_layer()
                compatibility_objects['MultiHeadAttention'] = create_compatible_attention_layer()
            
            # Remove None values
            compatibility_objects = {k: v for k, v in compatibility_objects.items() if v is not None}
            
            if compatibility_objects:
                model = keras.models.load_model(model_path, custom_objects=compatibility_objects, compile=False)
                print("✅ Model loaded with compatibility mapping")
                return model
            else:
                raise Exception("No compatible objects available")
                
        except Exception as e:
            print(f"❌ All loading methods failed: {e}")
            return None

def test_model_prediction(model, test_input_shape=(1, 128, 128, 3)):
    """
    Test if the model can make predictions without errors
    """
    try:
        print("🧪 Testing model prediction...")
        
        # Create a test input
        import numpy as np
        test_input = np.random.random(test_input_shape).astype(np.float32)
        
        # Make a prediction
        prediction = model.predict(test_input, verbose=0)
        
        print(f"✅ Model prediction successful. Output shape: {prediction.shape}")
        return True
        
    except Exception as e:
        print(f"❌ Model prediction failed: {e}")
        return False

def get_model_info(model):
    """
    Get information about the loaded model
    """
    if model is None:
        return "Model not loaded"
    
    try:
        info = {
            "input_shape": model.input_shape,
            "output_shape": model.output_shape,
            "num_layers": len(model.layers),
            "total_params": model.count_params(),
            "model_name": model.name if hasattr(model, 'name') else "Unknown"
        }
        return info
    except Exception as e:
        return f"Error getting model info: {e}"

# Compatibility classes for custom objects
class CompatibleSeqSelfAttention(keras.layers.Layer):
    """Compatible self-attention layer"""
    
    def __init__(self, head_num=8, activation='relu', use_bias=True, 
                 kernel_initializer='glorot_normal', bias_initializer='zeros',
                 kernel_regularizer=None, bias_regularizer=None,
                 kernel_constraint=None, bias_constraint=None,
                 history_only=False, **kwargs):
        super().__init__(**kwargs)
        
        # Store original parameters for compatibility
        self.head_num = head_num
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint
        self.history_only = history_only
        
        # Create compatible attention layer
        self.attention = keras.layers.MultiHeadAttention(
            num_heads=head_num,
            key_dim=64,  # Default key dimension
            dropout=0.1
        )
    
    def call(self, inputs, **kwargs):
        # For self-attention, query, key, and value are the same
        return self.attention(inputs, inputs, inputs)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'head_num': self.head_num,
            'activation': self.activation,
            'use_bias': self.use_bias,
            'kernel_initializer': self.kernel_initializer,
            'bias_initializer': self.bias_initializer,
            'kernel_regularizer': self.kernel_regularizer,
            'bias_regularizer': self.bias_regularizer,
            'kernel_constraint': self.kernel_constraint,
            'bias_constraint': self.bias_constraint,
            'history_only': self.history_only,
        })
        return config

class CompatibleMultiHeadAttention(keras.layers.Layer):
    """Compatible multi-head attention layer"""
    
    def __init__(self, head_num=8, activation='relu', use_bias=True,
                 kernel_initializer='glorot_normal', bias_initializer='zeros',
                 kernel_regularizer=None, bias_regularizer=None,
                 kernel_constraint=None, bias_constraint=None,
                 history_only=False, **kwargs):
        super().__init__(**kwargs)
        
        # Store original parameters for compatibility
        self.head_num = head_num
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint
        self.history_only = history_only
        
        # Create compatible attention layer
        self.attention = keras.layers.MultiHeadAttention(
            num_heads=head_num,
            key_dim=64,  # Default key dimension
            dropout=0.1
        )
    
    def call(self, inputs, **kwargs):
        if isinstance(inputs, (list, tuple)) and len(inputs) >= 3:
            query, key, value = inputs[0], inputs[1], inputs[2]
            return self.attention(query, key, value)
        else:
            # Fallback to self-attention
            return self.attention(inputs, inputs, inputs)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'head_num': self.head_num,
            'activation': self.activation,
            'use_bias': self.use_bias,
            'kernel_initializer': self.kernel_initializer,
            'bias_initializer': self.bias_initializer,
            'kernel_regularizer': self.kernel_regularizer,
            'bias_regularizer': self.bias_regularizer,
            'kernel_constraint': self.kernel_constraint,
            'bias_constraint': self.bias_constraint,
            'history_only': self.history_only,
        })
        return config

# Export compatibility objects
COMPATIBILITY_OBJECTS = {
    'SeqSelfAttention': CompatibleSeqSelfAttention,
    'MultiHeadAttention': CompatibleMultiHeadAttention,
}
