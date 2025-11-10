# Hair Disease Prediction - Django Integration

This project integrates your ML model for hair disease prediction with Django, allowing you to run both the web application and the ML model together seamlessly.

## 🚀 Quick Start

### Option 1: Using the Startup Scripts (Recommended)

**For Windows:**

```bash
start_app.bat
```

**For Linux/Mac:**

```bash
chmod +x start_app.sh
./start_app.sh
```

**For Python directly:**

```bash
python start_django_app.py
```

### Option 2: Manual Setup

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Navigate to Django Project:**

   ```bash
   cd minor
   ```

3. **Run Migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Start Django Server:**
   ```bash
   python manage.py runserver
   ```

## 📱 Access the Application

- **Main Application:** http://127.0.0.1:8000
- **ML Prediction Page:** http://127.0.0.1:8000/predict
- **Result Page:** http://127.0.0.1:8000/result
- **Admin Panel:** http://127.0.0.1:8000/admin

## 🏗️ Project Structure

```
disease prediction model/
├── minor/                          # Django project
│   ├── minor/                     # Django settings
│   │   ├── settings.py            # Updated with ML integration
│   │   └── urls.py                # URL patterns
│   ├── myapp/                     # Django app
│   │   ├── ml_service.py          # ML model service
│   │   ├── views.py               # Updated views with ML integration
│   │   └── templates/             # HTML templates
│   │       ├── predict.html       # Upload and prediction page
│   │       └── result.html        # Results display page
│   └── manage.py
├── hair-diseases.h5               # Your trained ML model
├── start_django_app.py            # Main startup script
├── start_app.bat                  # Windows batch file
├── start_app.sh                   # Linux/Mac shell script
└── requirements.txt               # Updated dependencies
```

## 🔧 Key Features

### 1. **Integrated ML Model**

- The ML model is loaded automatically when Django starts
- No need to run separate FastAPI server
- Model predictions are handled through Django views

### 2. **Django Templates**

- `predict.html`: Upload interface with image preview and zoom functionality
- `result.html`: Results display with disease information and PDF export

### 3. **API Endpoint**

- `/predict-api`: POST endpoint for ML predictions
- Accepts image files and returns JSON with prediction results

### 4. **Client Data Management**

- Client information is stored in browser localStorage
- Seamless data flow between upload and result pages

## 🛠️ Technical Details

### ML Service (`ml_service.py`)

- Loads the trained model with custom attention layers
- Handles image preprocessing (resize to 128x128, normalize)
- Returns prediction results with confidence scores

### Django Views

- `predict()`: Renders the upload page
- `predict_api()`: Handles ML prediction requests
- `result()`: Renders the results page

### Frontend Integration

- Uses Tailwind CSS for styling
- JavaScript handles image preview, zoom, and API calls
- PDF generation for reports using jsPDF

## 🔄 How It Works

1. **User uploads image** on `/predict` page
2. **Client details** are collected (name, DOB, contact)
3. **Image is sent** to `/predict-api` endpoint
4. **ML model processes** the image and returns prediction
5. **Results are stored** in localStorage
6. **User is redirected** to `/result` page
7. **Results are displayed** with disease information and PDF export option

## 🐛 Troubleshooting

### Common Issues:

1. **Model not loading:**

   - Ensure `hair-diseases.h5` is in the project root
   - Check that all ML dependencies are installed

2. **Django server not starting:**

   - Run migrations: `python manage.py migrate`
   - Check for port conflicts (default port 8000)

3. **Prediction errors:**
   - Verify image format (JPG, PNG, JPEG)
   - Check file size (should be under 10MB)

### Debug Mode:

- Django runs in debug mode by default
- Check console output for detailed error messages
- ML model loading status is displayed in console

## 📦 Dependencies

The project now includes both ML and Django dependencies:

- **ML Dependencies:** TensorFlow, Keras, NumPy, Pillow, etc.
- **Django Dependencies:** Django, DRF, CORS headers
- **Optional:** FastAPI (for standalone API if needed)

## 🎯 Benefits of This Integration

1. **Single Server:** No need to run separate FastAPI and Django servers
2. **Unified Interface:** All functionality accessible through Django
3. **Easy Deployment:** Standard Django deployment process
4. **Better Security:** Django's built-in security features
5. **Scalability:** Can easily add more features and pages

## 🚀 Next Steps

1. **Customize Templates:** Modify the HTML templates to match your design
2. **Add Authentication:** Implement user login/registration
3. **Database Storage:** Store prediction history in database
4. **Admin Interface:** Use Django admin for managing data
5. **API Documentation:** Add API documentation if needed

## 📞 Support

If you encounter any issues:

1. Check the console output for error messages
2. Ensure all dependencies are installed
3. Verify the model file is in the correct location
4. Check Django logs for detailed error information

---

**Note:** This integration maintains all the original functionality of your ML model while providing a robust web framework for the user interface.
