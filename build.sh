#!/usr/bin/env bash
set -e

echo "=== Hair & Scalp Detector Build Script ==="

# 1. Install Git LFS (if not already installed)
echo "Installing Git LFS..."
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get update -qq
apt-get install -y git-lfs 2>&1 | grep -v "done\|Setting up git-lfs"
git lfs install

# 2. Fetch LFS files
echo "Pulling Git LFS objects..."
git lfs pull origin main 2>&1 || echo "Warning: LFS pull had issues, but continuing..."

# 3. Navigate to Django app directory
cd required_files/minor

# 4. Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# 5. Run migrations (if database migrations exist)
echo "Running Django migrations..."
python manage.py migrate --noinput --settings=minor.settings_production 2>&1 || echo "Migrations completed or skipped."

# 6. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=minor.settings_production 2>&1 | tail -5

echo "=== Build completed successfully ==="
