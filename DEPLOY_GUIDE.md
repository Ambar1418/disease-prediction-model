# Deployment Guide: Hair & Scalp Detector

## Quick Start (Render)

### 1. Prerequisites
- Git LFS installed on your machine (for pushing large model files)
- A Render account (https://render.com)
- GitHub account with the repository push access

### 2. Push to GitHub with LFS
Before deploying to Render, ensure Git LFS is tracking your model files:

```bash
# Install Git LFS locally (if not already)
brew install git-lfs          # macOS
# or apt-get install git-lfs  # Linux

# Initialize Git LFS in your repo (one time)
git lfs install

# Track large files (already done if in .gitattributes)
git lfs track "*.pth"
git lfs track "*.h5"
git add .gitattributes

# Push to GitHub (includes LFS files)
git add .
git commit -m "Deploy with LFS"
git push origin main
```

### 3. Deploy to Render

#### Option A: Using render-cli (fastest)
```bash
# Install render CLI
npm i -g @render-com/cli

# Login
render login

# Deploy from the render_deploy.yaml file
render deploy --file render_deploy.yaml
```

#### Option B: Using Render Dashboard (manual)
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Select your GitHub repository (`hair-scalp-detector`)
4. Fill in settings:
   - **Name**: `hair-scalp-detector-api`
   - **Environment**: `Python`
   - **Python Version**: `3.11`
   - **Build Command**:
     ```bash
     set -e
     curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
     apt-get update -qq && apt-get install -y git-lfs
     git lfs install && git lfs pull origin main || true
     cd required_files/minor
     pip install -q -r requirements.txt
     python manage.py migrate --noinput --settings=minor.settings_production || true
     python manage.py collectstatic --noinput --settings=minor.settings_production
     ```
   - **Start Command**:
     ```bash
     cd required_files/minor && gunicorn minor.wsgi:application --bind 0.0.0.0:$PORT --timeout 600 --workers 2
     ```
   - **Plan**: Starter (or higher)
   - **Environment Variables**:
     - `DJANGO_SETTINGS_MODULE`: `minor.settings_production`
     - `SECRET_KEY`: Generate a new Django secret key or use your existing one
5. Click "Create Web Service"
6. Wait for the build to complete (~3-5 minutes)

### 4. Verify Deployment
Once Render shows "Live", test the API:

```bash
# Replace with your Render URL (e.g., hair-scalp-detector.onrender.com)
RENDER_URL="https://hair-scalp-detector.onrender.com"

# Test home page
curl -I $RENDER_URL/

# Test API endpoint
curl -i $RENDER_URL/check-auth

# Test predict endpoint (requires login/auth)
curl -X POST $RENDER_URL/predict-api \
  -F "file=@sample_image.jpg" \
  -F "symptom_start_date=2025-11-01"
```

### 5. Connect Vercel Frontend

Once Render API is live, update `vercel.json` with the Render URL:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "required_files/frontend/index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://hair-scalp-detector.onrender.com/:splat"
    },
    {
      "src": "/(.*)",
      "dest": "/required_files/frontend/index.html"
    }
  ]
}
```

Then redeploy Vercel frontend and test both frontend + backend together.

## Troubleshooting

### Git LFS Error During Build
If you see `error: external filter 'git-lfs filter-process' failed`:
1. Ensure Git LFS is installed in the build image (build command includes `apt-get install git-lfs`).
2. Check if you've exceeded GitHub LFS bandwidth quota (Settings → Plans → LFS).
3. Alternative: Download the model from a URL at runtime (see below).

### Missing Static Files Error
If you see `ValueError: Missing staticfiles manifest entry for 'images/favicon.png'`:
1. Ensure `python manage.py collectstatic` runs in the build command (it does).
2. Use `CompressedStaticFilesStorage` instead of `CompressedManifestStaticFilesStorage` in `settings_production.py` (already updated).

### Partial Checkout / Directory Exists Error
If `/opt/render/project/src` already exists:
1. In Render dashboard, click "Clear Build Cache" and redeploy.
2. Or delete the service and create a new one.

## Production Checklist
- [ ] Set `SECRET_KEY` environment variable in Render (Settings > Environment)
- [ ] Update `ALLOWED_HOSTS` in `settings_production.py` with your Render domain
- [ ] Update `CORS_ALLOWED_ORIGINS` with your Vercel frontend URL
- [ ] Enable HTTPS (Render provides free Let's Encrypt certificates)
- [ ] Set up PostgreSQL database if using more than SQLite (SQLite works for small deployments)
- [ ] Test `/api/check-auth` and `/predict-api` endpoints before going live
- [ ] Monitor logs: Render Dashboard → Service → Logs

## Optional: Store Model Files Externally (Recommended for Production)

If LFS causes issues, consider uploading the model to S3 and downloading at runtime:

```bash
# Upload model to AWS S3
aws s3 cp required_files/best_model.pth s3://my-bucket/models/best_model.pth --acl public-read

# Update ml_service.py to download at startup
# (See ml_service.py for example)
```

Then update the build command to skip LFS:
```bash
cd required_files/minor
pip install -q -r requirements.txt
python manage.py migrate --noinput --settings=minor.settings_production || true
python manage.py collectstatic --noinput --settings=minor.settings_production
# Remove git lfs pull from build
```

This avoids LFS dependencies entirely.
