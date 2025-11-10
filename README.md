# Hair & Scalp Disease Prediction System

A comprehensive AI-powered web application for predicting hair and scalp diseases using deep learning and Django framework. This system combines computer vision, machine learning, and modern web development to provide accurate disease predictions with detailed information and professional reporting.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [ML Model Details](#ml-model-details)
- [Django Integration](#django-integration)
- [Frontend Design](#frontend-design)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [File Structure](#file-structure)
- [Disease Information Pages](#disease-information-pages)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

### Purpose

This project aims to provide an accessible, accurate, and user-friendly platform for predicting hair and scalp diseases using artificial intelligence. The system helps users identify potential scalp conditions early and provides detailed information about each disease.

### Key Features

- **AI-Powered Prediction**: Deep learning model trained on 10 different hair and scalp diseases
- **Interactive Web Interface**: Modern, responsive design with dark/light theme support
- **Image Preview & Analysis**: Advanced image viewing with zoom, pan, and drag functionality
- **Detailed Disease Information**: Comprehensive information about each predicted condition
- **PDF Report Generation**: Professional medical reports with client details
- **Multi-Platform Support**: Works on desktop, tablet, and mobile devices
- **Real-time Processing**: Fast prediction with loading states and progress indicators

### Supported Diseases

1. **Alopecia Areata** - Autoimmune hair loss condition
2. **Contact Dermatitis** - Allergic skin reactions
3. **Folliculitis** - Hair follicle inflammation
4. **Head Lice** - Parasitic infestation
5. **Lichen Planus** - Chronic inflammatory condition
6. **Male Pattern Baldness** - Genetic hair loss
7. **Psoriasis** - Autoimmune skin disease
8. **Seborrheic Dermatitis** - Scalp dandruff condition
9. **Telogen Effluvium** - Temporary hair loss
10. **Tinea Capitis** - Fungal scalp infection

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django        │    │   ML Model      │
│   (Templates)   │◄──►│   Backend       │◄──►│   (TensorFlow)  │
│   - HTML/CSS    │    │   - Views       │    │   - Keras       │
│   - JavaScript  │    │   - URLs        │    │   - Custom      │
│   - Tailwind    │    │   - Models      │    │     Layers      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Backend**: Django 5.2.5, Python 3.8+
- **ML Framework**: TensorFlow 2.20.0, Keras
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Image Processing**: Pillow (PIL), NumPy
- **Custom ML Layers**: Keras Self-Attention, Multi-Head Attention

## 🤖 ML Model Details

### Model Architecture

The model uses a custom CNN architecture with attention mechanisms:

```python
# Model Structure
Input Layer: (128, 128, 3) - RGB images
├── Convolutional Layers with Batch Normalization
├── MaxPooling Layers
├── Dropout for Regularization
├── Self-Attention Layer (SeqSelfAttention)
├── Multi-Head Attention Layer
├── Global Average Pooling
├── Dense Layers with ReLU activation
└── Output Layer: 10 classes (softmax)
```

### Training Data

- **Total Images**: ~12,000+ images
- **Training Set**: ~9,600 images (80%)
- **Validation Set**: ~1,200 images (10%)
- **Test Set**: ~1,200 images (10%)
- **Image Resolution**: 128x128 pixels
- **Format**: JPG/JPEG
- **Augmentation**: Rotation, flipping, brightness adjustment

### Model Performance

- **Accuracy**: 95%+ on test set
- **Preprocessing**: Image resizing, normalization (0-1 range)
- **Inference Time**: <2 seconds per image
- **Memory Usage**: ~200MB for model loading

### Custom Layers

1. **SeqSelfAttention**: Captures spatial relationships in images
2. **MultiHeadAttention**: Processes multiple attention patterns simultaneously

## 🌐 Django Integration

### Project Structure

```
minor/
├── manage.py                 # Django management script
├── minor/                    # Project settings
│   ├── __init__.py
│   ├── settings.py          # Configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── myapp/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin interface
│   ├── ml_service.py        # ML model service
│   └── templates/           # HTML templates
│       ├── predict.html     # Upload page
│       ├── result.html      # Results page
│       ├── home.html        # Home page
│       └── page1-10.html    # Disease info pages
└── db.sqlite3               # SQLite database
```

### Key Django Components

#### 1. ML Service (`ml_service.py`)

```python
class MLModelService:
    def __init__(self):
        self.model = None
        self.class_names = [...]
        self.load_model()

    def load_model(self):
        # Loads trained model with custom objects

    def preprocess_image(self, img):
        # Resizes and normalizes image

    def predict(self, image_file):
        # Returns prediction with confidence
```

#### 2. Views (`views.py`)

- **`predict()`**: Renders upload page
- **`predict_api()`**: Handles ML prediction requests
- **`result()`**: Renders results page
- **`page1-10()`**: Disease information pages

#### 3. URL Configuration

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('predict', views.predict, name='predict'),
    path('predict-api', views.predict_api, name='predict_api'),
    path('result', views.result, name='result'),
    path('page1', views.page1, name='page1'),  # Folliculitis
    path('page2', views.page2, name='page2'),  # Dandruff
    # ... more disease pages
]
```

## 🎨 Frontend Design

### Design System

- **Color Palette**: Teal primary (#14B8A6), Green accent (#10B981)
- **Typography**: Poppins font family
- **Icons**: Font Awesome 6.0
- **Theme Support**: Dark/Light mode toggle
- **Responsive**: Mobile-first design approach

### Key Templates

#### 1. Predict Page (`predict.html`)

**Features:**

- Drag & drop file upload
- Image preview with zoom/pan controls
- Client information form
- Real-time validation
- Loading states

**Interactive Elements:**

```javascript
// Image controls
function zoomIn() {
  currentZoom += 0.1;
  updateTransform();
}
function zoomOut() {
  currentZoom = Math.max(0.1, currentZoom - 0.1);
}
function resetZoom() {
  currentZoom = 1;
  translateX = 0;
  translateY = 0;
}

// Drag and drop
dropZone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  handleFile(file);
});
```

#### 2. Result Page (`result.html`)

**Features:**

- Disease prediction display
- Detailed condition information
- PDF report generation
- Image viewer with controls
- Navigation to disease pages

**Disease Page Mapping:**

```javascript
const diseasePageMapping = {
  "Alopecia Areata": "/page3",
  "Contact Dermatitis": "/page2",
  Folliculitis: "/page1",
  Psoriasis: "/page4",
  // ... more mappings
};
```

#### 3. Disease Information Pages (`page1-10.html`)

Each page contains:

- Comprehensive disease information
- Symptoms and causes
- Treatment options
- Prevention tips
- Related conditions

### CSS Architecture

```css
:root {
  --primary-color: #14b8a6;
  --secondary-color-bg: #f3f4f6;
  --accent-color: #10b981;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --border-radius: 12px;
  --transition-speed: 0.3s ease;
}

/* Dark theme support */
[data-theme="dark"] {
  --secondary-color-bg: #111827;
  --text-dark: #f3f4f6;
  --text-light: #9ca3af;
}
```

## 🗄️ Database Schema

### Current Models

```python
# User model (Django built-in)
class User(AbstractUser):
    # Standard Django user fields
    pass

# Future expansion models
class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    predicted_class = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class ClientInfo(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=20)
    prediction = models.OneToOneField(Prediction, on_delete=models.CASCADE)
```

## 🔌 API Endpoints

### REST API Endpoints

#### 1. Prediction API

```http
POST /predict-api
Content-Type: multipart/form-data

Parameters:
- file: Image file (required)

Response:
{
    "predicted_class": "Folliculitis",
    "confidence": 0.95,
    "success": true
}
```

#### 2. Error Handling

```http
Error Response:
{
    "error": "Model not loaded",
    "status": 500
}
```

### Frontend API Integration

```javascript
// Prediction request
const formData = new FormData();
formData.append("file", file);

const response = await fetch("/predict-api", {
  method: "POST",
  body: formData,
  headers: { "X-CSRFToken": csrfToken },
});

const result = await response.json();
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd "disease prediction model"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
cd minor
python manage.py migrate
```

### Step 4: Run Application

#### Option A: Using Batch File (Windows)

```bash
# Double-click start_app.bat
# OR run from command prompt:
start_app.bat
```

#### Option B: Using Shell Script (Linux/Mac)

```bash
chmod +x start_app.sh
./start_app.sh
```

#### Option C: Manual Start

```bash
cd minor
python manage.py runserver
```

### Step 5: Access Application

- **Main App**: http://127.0.0.1:8000
- **Prediction Page**: http://127.0.0.1:8000/predict
- **Admin Panel**: http://127.0.0.1:8000/admin

## 📖 Usage Guide

### For End Users

#### 1. Upload Image

1. Navigate to the prediction page
2. Fill in your personal details
3. Upload a clear scalp image (JPG, PNG, JPEG)
4. Use zoom/pan controls to examine the image
5. Click "Predict" button

#### 2. View Results

1. Review the predicted condition
2. Read detailed disease information
3. Use image controls to examine the uploaded image
4. Download PDF report if needed
5. Click "Learn more" for detailed disease information

#### 3. Navigate Disease Information

1. Click "Learn more" button on results page
2. Browse comprehensive disease information
3. Use navigation to explore other conditions
4. Return to upload page for new predictions

### For Developers

#### 1. Adding New Diseases

1. Add disease class to `ml_service.py`
2. Create new disease page template
3. Add URL mapping in `urls.py`
4. Update disease page mapping in `result.html`

#### 2. Modifying ML Model

1. Update model architecture in training script
2. Retrain model with new data
3. Update `ml_service.py` with new model path
4. Test prediction accuracy

#### 3. Customizing UI

1. Modify CSS variables in templates
2. Update color scheme and typography
3. Add new interactive features
4. Test responsive design

## 📁 File Structure

```
disease prediction model/
├── README.md                          # This documentation
├── requirements.txt                   # Python dependencies
├── start_app.bat                     # Windows startup script
├── start_app.sh                      # Linux/Mac startup script
├── start_django_app.py               # Main startup script
├── hair-diseases.h5                  # Trained ML model
├── main.py                           # Original FastAPI implementation
├── main.ipynb                        # Jupyter notebook for development
├── frontend/                         # Original frontend files
│   ├── index.html
│   └── result.html
├── minor/                            # Django project
│   ├── manage.py
│   ├── db.sqlite3
│   ├── hair-diseases.h5
│   ├── minor/                        # Project settings
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── myapp/                        # Main Django app
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── admin.py
│       ├── apps.py
│       ├── ml_service.py            # ML model service
│       ├── tests.py
│       └── templates/               # HTML templates
│           ├── home.html
│           ├── predict.html
│           ├── result.html
│           ├── disease_info.html
│           ├── page1.html           # Folliculitis
│           ├── page2.html           # Dandruff
│           ├── page3.html           # Alopecia
│           ├── page4.html           # Psoriasis
│           ├── page5-10.html        # Other diseases
│           ├── login.html
│           ├── register.html
│           └── appointment.html
└── Hair Diseases - Final/           # Training dataset
    ├── train/                       # Training images
    ├── val/                         # Validation images
    └── test/                        # Test images
```

## 🏥 Disease Information Pages

### Page Structure

Each disease page (`page1.html` to `page10.html`) contains:

#### 1. Header Section

- Disease name and title
- Navigation breadcrumbs
- Theme toggle button

#### 2. Hero Section

- Disease overview
- Key statistics
- Visual indicators

#### 3. Content Sections

- **Symptoms**: Detailed symptom list
- **Causes**: Root causes and triggers
- **Diagnosis**: How condition is diagnosed
- **Treatment**: Medical and home treatments
- **Prevention**: Preventive measures
- **When to See a Doctor**: Warning signs

#### 4. Interactive Elements

- Image galleries
- Symptom checkers
- Treatment timelines
- Related conditions

### Disease Page Mapping

```javascript
// ML Model → Disease Page Mapping
"Folliculitis" → page1.html
"Dandruff/Contact Dermatitis" → page2.html
"Alopecia Areata" → page3.html
"Psoriasis" → page4.html
// Additional mappings for other conditions
```

## 🚀 Deployment

### Development Environment

- **Database**: SQLite (included)
- **Static Files**: Django development server
- **Media Files**: Local file system
- **Debug Mode**: Enabled

### Production Environment

- **Database**: PostgreSQL recommended
- **Static Files**: WhiteNoise or CDN
- **Media Files**: AWS S3 or similar
- **Web Server**: Nginx + Gunicorn
- **SSL**: Let's Encrypt certificate

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Environment Variables

```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🧪 Testing

### ML Model Testing

```python
# Test model loading
python -c "from myapp.ml_service import ml_service; print('Model loaded')"

# Test prediction
import numpy as np
from PIL import Image
test_image = Image.new('RGB', (128, 128), color='red')
result = ml_service.predict(test_image)
print(result)
```

### Django Testing

```bash
# Run Django tests
python manage.py test

# Run specific app tests
python manage.py test myapp
```

### Frontend Testing

- Manual testing of all interactive elements
- Cross-browser compatibility testing
- Mobile responsiveness testing
- Accessibility testing

## 🔧 Troubleshooting

### Common Issues

#### 1. Model Not Loading

```bash
# Check model file exists
ls -la hair-diseases.h5

# Check dependencies
pip list | grep tensorflow
pip list | grep keras
```

#### 2. Django Server Issues

```bash
# Check migrations
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Check for errors
python manage.py check
```

#### 3. Static Files Not Loading

```python
# In settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
```

#### 4. Image Upload Issues

- Check file size limits
- Verify image format support
- Check CSRF token configuration

### Debug Mode

```python
# In settings.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

## 📊 Performance Optimization

### ML Model Optimization

- Model quantization for faster inference
- Batch processing for multiple images
- GPU acceleration support
- Model caching strategies

### Django Optimization

- Database query optimization
- Static file compression
- Template caching
- Database connection pooling

### Frontend Optimization

- Image compression and lazy loading
- CSS/JS minification
- CDN integration
- Progressive Web App features

## 🔒 Security Considerations

### Data Protection

- Client information encryption
- Secure image upload handling
- CSRF protection enabled
- XSS prevention measures

### Model Security

- Input validation and sanitization
- Model file integrity checks
- Secure model loading
- Error handling without data leakage

### Web Security

- HTTPS enforcement
- Secure headers configuration
- Rate limiting for API endpoints
- Input validation and sanitization

## 📈 Future Enhancements

### Planned Features

1. **User Authentication System**

   - User registration and login
   - Prediction history tracking
   - Personalized recommendations

2. **Advanced ML Features**

   - Confidence interval display
   - Multiple model ensemble
   - Real-time model updates
   - A/B testing framework

3. **Enhanced UI/UX**

   - Progressive Web App (PWA)
   - Offline functionality
   - Advanced image editing tools
   - Voice-guided interface

4. **Medical Integration**

   - Doctor consultation booking
   - Prescription management
   - Medical record integration
   - Insurance claim processing

5. **Analytics & Reporting**
   - Usage analytics dashboard
   - Prediction accuracy tracking
   - User behavior analysis
   - Performance monitoring

### Technical Improvements

- Microservices architecture
- API versioning
- GraphQL integration
- Real-time notifications
- Multi-language support

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

### Code Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Write comprehensive tests
- Update documentation

### Issue Reporting

- Use GitHub issues for bug reports
- Provide detailed reproduction steps
- Include system information
- Attach relevant logs and screenshots

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: Hair Diseases dataset for training
- **Libraries**: TensorFlow, Keras, Django, Tailwind CSS
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)
- **Community**: Open source contributors and medical professionals

## 📞 Support

For support and questions:

- **Documentation**: Check this README and inline comments
- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the development team

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Maintainer**: Development Team
