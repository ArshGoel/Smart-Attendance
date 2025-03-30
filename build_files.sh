echo "BUILD START"

# Install dependencies
# python -m pip install --upgrade pip
python3 -m pip install --no-cache-dir django whitenoise opencv-python cmake face-recognition 

# Collect static files
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
