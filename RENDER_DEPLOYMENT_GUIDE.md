# Render Deployment Guide for Disease Prediction App

## Deployment Configuration

### 1. Root Directory
```
/
```

### 2. Build Command
```
pip install -r required_files/requirements_production.txt && python required_files/manage.py collectstatic --noinput
```

### 3. Start Command
```
gunicorn minor.wsgi:application --log-file -
```

### 4. Environment Variables
```
PYTHON_VERSION=3.10.12
DJANGO_SETTINGS_MODULE=minor.settings
SECRET_KEY=your-secret-key-here
DISABLE_COLLECTSTATIC=0
```

### 5. Python Version
```
3.10.12
```

## Required Files

1. `render.yaml` (already created in the root directory)
2. `requirements_production.txt` (already exists in required_files/)
3. `Procfile` (will be created automatically by Render)

## Deployment Steps

1. **Create a new Web Service on Render**
   - Go to https://dashboard.render.com/
   - Click "New" and select "Web Service"
   - Connect your GitHub/GitLab repository or use manual deploy

2. **Configure the service**
   - Name: `disease-prediction-app` (or your preferred name)
   - Region: Choose the closest to your users
   - Branch: `main` (or your main branch)
   - Root Directory: `/`
   - Build Command: (as shown above)
   - Start Command: (as shown above)
   - Plan: Free (or upgrade for better performance)

3. **Set Environment Variables**
   - Add all environment variables listed above
   - Generate a new `SECRET_KEY` if you don't have one

4. **Deploy**
   - Click "Create Web Service"
   - Monitor the build logs for any issues

## Post-Deployment Checklist

- [ ] Verify the application is running by visiting the provided URL
- [ ] Check the logs for any errors
- [ ] Test the API endpoints if applicable
- [ ] Set up a custom domain if needed
- [ ] Configure SSL/TLS (automatically handled by Render)
- [ ] Set up auto-deploy for your main branch

## Troubleshooting

1. **Static files not loading?**
   - Ensure `whitenoise` is in your requirements
   - Check that `STATIC_ROOT` is set in settings.py
   - Verify the build process completes the collectstatic step

2. **Application not starting?**
   - Check the logs for Python errors
   - Verify all environment variables are set correctly
   - Ensure the database URL is correct if using a database

3. **Build failing?**
   - Check for missing dependencies in requirements_production.txt
   - Ensure the Python version is compatible with your dependencies
   - Look for any compilation errors in the build logs

## Security Notes

1. Never commit your `SECRET_KEY` to version control
2. Use environment variables for sensitive information
3. Keep your dependencies updated
4. Regularly check for security updates

## Next Steps

1. Set up a CI/CD pipeline
2. Configure monitoring and alerts
3. Set up a staging environment
4. Implement database backups

For more information, refer to the [Render documentation](https://render.com/docs).
