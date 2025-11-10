# Hair Disease Prediction Model - macOS Edition

🍎 **Optimized for Apple Silicon (M1/M2/M3) Macs with Metal Performance Shaders**

This project provides a machine learning-based hair disease classification system with a web interface, specifically optimized for macOS environments.

## Features

- **10 Hair Disease Classifications**: Alopecia Areata, Contact Dermatitis, Folliculitis, Head Lice, Lichen Planus, Male Pattern Baldness, Psoriasis, Seborrheic Dermatitis, Telogen Effluvium, Tinea Capitis
- **Web Interface**: Django-based user-friendly web application
- **FastAPI Support**: Standalone API server with automatic documentation
- **Metal GPU Acceleration**: Optimized for Apple Silicon with Metal Performance Shaders
- **User Authentication**: Login/registration system
- **Cross-Platform**: Works on Intel and Apple Silicon Macs

## System Requirements

### Hardware

- **macOS**: 10.15 (Catalina) or later
- **RAM**: Minimum 8GB (16GB recommended for optimal performance)
- **Storage**: 2GB free space
- **Processor**: Intel x64 or Apple Silicon (M1/M2/M3)

### Software

- **Python**: 3.8+ (3.11 recommended)
- **Homebrew**: For easy package management (optional but recommended)

## Quick Start

### 1. Automated Installation (Recommended)

```bash
# Make the installation script executable
chmod +x install_macos.sh

# Run the automated installation
./install_macos.sh
```

### 2. Manual Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install macOS-specific dependencies
pip install -r requirements-macos.txt

# Start the application
./start_app.sh
```

## Running the Application

### Django Web Application

```bash
# Start Django server
./start_app.sh
# or
./start_macos.sh
```

Access at: http://127.0.0.1:8000

### FastAPI Standalone Server

```bash
# Start FastAPI server
./start_fastapi_macos.sh
# or
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Access at: http://127.0.0.1:8000/docs

## macOS-Specific Optimizations

### Apple Silicon (M1/M2/M3) Optimizations

- **TensorFlow-macOS**: Optimized TensorFlow build for Apple Silicon
- **Metal Performance Shaders**: GPU acceleration using Apple's Metal framework
- **Memory Management**: Optimized memory usage for Apple Silicon architecture
- **Thread Optimization**: Configured for Apple Silicon's unified memory architecture

### Intel Mac Optimizations

- **CPU Optimization**: Multi-threading configuration for Intel processors
- **Memory Management**: Optimized for Intel Mac memory architecture
- **Fallback Support**: Graceful degradation when Metal GPU is not available

## Dependencies

### Core Dependencies

- **Django 5.2.5**: Web framework
- **TensorFlow-macOS 2.16.1**: Machine learning framework (Apple Silicon optimized)
- **TensorFlow-Metal 1.2.0**: Metal GPU acceleration
- **FastAPI 0.104.1**: Modern API framework
- **Uvicorn**: ASGI server
- **Pillow**: Image processing
- **NumPy**: Numerical computing

### Optional Dependencies

- **psutil**: System monitoring and optimization
- **keras-self-attention**: Custom attention layers
- **keras-multi-head**: Multi-head attention layers

## File Structure

```
disease prediction model/
├── install_macos.sh          # macOS installation script
├── start_macos.sh           # macOS Django startup script
├── start_fastapi_macos.sh   # macOS FastAPI startup script
├── requirements-macos.txt   # macOS-specific dependencies
├── main.py                  # FastAPI application
├── start_django_app.py      # Django startup script
├── hair-diseases.h5         # Trained ML model
├── minor/                   # Django project
│   ├── manage.py
│   ├── minor/
│   │   ├── settings.py
│   │   └── urls.py
│   └── myapp/
│       ├── ml_service.py    # ML service with macOS optimizations
│       ├── views.py
│       └── templates/
└── frontend/                # Static frontend files
    ├── index.html
    └── result.html
```

## Troubleshooting

### Common Issues

#### 1. TensorFlow Installation Fails

```bash
# Try installing with specific versions
pip install tensorflow-macos==2.16.1 tensorflow-metal==1.2.0

# If still failing, use CPU-only version
pip install tensorflow==2.16.1
```

#### 2. Metal GPU Not Detected

- Ensure you're using Apple Silicon (M1/M2/M3)
- Check macOS version (10.15+ required)
- Verify TensorFlow-Metal installation

#### 3. Port 8000 Already in Use

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

#### 4. Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-macos.txt
```

#### 5. Model Loading Errors

- Ensure `hair-diseases.h5` is in the project root
- Check file permissions
- Verify model file integrity

### Performance Optimization

#### For Apple Silicon Macs

- Enable Metal GPU acceleration (automatic)
- Use `requirements-macos.txt` for optimal packages
- Ensure sufficient RAM (16GB+ recommended)

#### For Intel Macs

- Use CPU-optimized TensorFlow
- Adjust thread count in environment variables
- Monitor CPU usage during predictions

## Development

### Adding New Features

1. Modify `minor/myapp/views.py` for Django features
2. Update `main.py` for FastAPI endpoints
3. Test on both Intel and Apple Silicon Macs

### Model Updates

1. Replace `hair-diseases.h5` with new model
2. Update class names in `ml_service.py` and `main.py`
3. Test prediction accuracy

## API Documentation

### FastAPI Endpoints

- **POST /predict**: Upload image for disease classification
- **GET /docs**: Interactive API documentation
- **GET /health**: Health check endpoint

### Django URLs

- **/**: Home page
- **/predict**: Prediction interface
- **/admin**: Django admin panel
- **/accounts/login**: User login
- **/accounts/register**: User registration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test on macOS (both Intel and Apple Silicon)
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For macOS-specific issues:

- Check the installation logs
- Verify Python and TensorFlow versions
- Test with both Django and FastAPI servers
- Monitor system resources during operation

## Performance Benchmarks

### Apple Silicon (M1 Pro)

- **Model Loading**: ~2-3 seconds
- **Prediction Time**: ~0.5-1 second per image
- **Memory Usage**: ~2-4GB during operation

### Intel Mac (i7)

- **Model Loading**: ~3-5 seconds
- **Prediction Time**: ~1-2 seconds per image
- **Memory Usage**: ~3-5GB during operation

---

🍎 **Enjoy using Hair Disease Prediction on macOS!**
