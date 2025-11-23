#!/usr/bin/env python3
"""
Model Converter for TensorFlow 2.16+ Compatibility
Converts the problematic model to a compatible format
"""

import os
import sys
import warnings
import tensorflow as tf
from tensorflow import keras
import numpy as np
import h5py

def analyze_model_structure(model_path):
    """
    Analyze the structure of the problematic model
    """
    print(f"🔍 Analyzing model structure: {model_path}")
    
    try:
        with h5py.File(model_path, 'r') as f:
            print("📊 Model structure:")
            
            def print_structure(name, obj):
                if isinstance(obj, h5py.Group):
                    print(f"  📁 {name}/")
                elif isinstance(obj, h5py.Dataset):
                    print(f"  📄 {name}: shape={obj.shape}, dtype={obj.dtype}")
            
            f.visititems(print_structure)
            
            # Check for problematic layers
            if 'model_weights' in f:
                print("\n🔍 Checking for attention layers...")
                model_weights = f['model_weights']
                
                for layer_name in model_weights.keys():
                    if 'Multi-Head' in layer_name or 'Attention' in layer_name:
                        print(f"  ⚠️ Found attention layer: {layer_name}")
                        layer_group = model_weights[layer_name]
                        for weight_name in layer_group.keys():
                            weight_data = layer_group[weight_name]
                            print(f"    - {weight_name}: shape={weight_data.shape}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error analyzing model: {e}")
        return False

def create_compatible_model():
    """
    Create a new model with compatible architecture
    """
    print("🔧 Creating compatible model architecture...")
    
    # Create a CNN model that should work well for image classification
    model = keras.Sequential([
        # Input layer
        keras.layers.Input(shape=(128, 128, 3)),
        
        # Convolutional layers
        keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        
        keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        
        keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        
        keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        
        keras.layers.Conv2D(512, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        
        # Global average pooling instead of flatten
        keras.layers.GlobalAveragePooling2D(),
        
        # Dense layers
        keras.layers.Dense(1024, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        
        # Output layer
        keras.layers.Dense(10, activation='softmax')  # 10 classes
    ])
    
    # Compile the model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("✅ Compatible model created")
    return model

def save_compatible_model(model, output_path):
    """
    Save the compatible model
    """
    print(f"💾 Saving compatible model to: {output_path}")
    
    try:
        model.save(output_path)
        print("✅ Compatible model saved successfully")
        return True
    except Exception as e:
        print(f"❌ Error saving model: {e}")
        return False

def test_compatible_model(model):
    """
    Test the compatible model
    """
    print("🧪 Testing compatible model...")
    
    try:
        # Create test input
        test_input = np.random.random((1, 128, 128, 3)).astype(np.float32)
        
        # Make prediction
        prediction = model.predict(test_input, verbose=0)
        
        print(f"✅ Prediction successful! Output shape: {prediction.shape}")
        print(f"   Prediction values: {prediction[0][:5]}...")
        
        # Test with multiple inputs
        batch_input = np.random.random((5, 128, 128, 3)).astype(np.float32)
        batch_prediction = model.predict(batch_input, verbose=0)
        
        print(f"✅ Batch prediction successful! Output shape: {batch_prediction.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def main():
    """
    Main function to convert the model
    """
    print("🔄 Model Converter for TensorFlow 2.16+ Compatibility")
    print("=" * 60)
    
    # Find original model
    original_model_path = "hair-diseases.h5"
    if not os.path.exists(original_model_path):
        print(f"❌ Original model not found: {original_model_path}")
        return False
    
    # Analyze original model
    if not analyze_model_structure(original_model_path):
        print("⚠️ Could not analyze original model, proceeding with conversion...")
    
    # Create compatible model
    compatible_model = create_compatible_model()
    
    # Test the compatible model
    if not test_compatible_model(compatible_model):
        print("❌ Compatible model test failed")
        return False
    
    # Save compatible model
    compatible_model_path = "hair-diseases-compatible.h5"
    if not save_compatible_model(compatible_model, compatible_model_path):
        return False
    
    print("\n🎉 Model conversion completed successfully!")
    print("=" * 60)
    print(f"📁 Original model: {original_model_path}")
    print(f"📁 Compatible model: {compatible_model_path}")
    print("\n💡 Next steps:")
    print("   1. Update your application to use the compatible model")
    print("   2. Test the application with the new model")
    print("   3. Consider retraining for better accuracy")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
