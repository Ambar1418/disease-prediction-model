import os
import requests
import sys

def download_model():
    model_url = "https://github.com/Ambar1418/disease-prediction-model/raw/main/hair-diseases-compatible.h5"
    model_path = os.path.join("required_files", "hair-diseases-compatible.h5")
    
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}")
        return
    
    print(f"Downloading model from {model_url}...")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    try:
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Successfully downloaded model to {model_path}")
    except Exception as e:
        print(f"Error downloading model: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    download_model()
