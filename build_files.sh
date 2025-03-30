echo "BUILD START"

# Upgrade pip
python3 -m pip install --upgrade pip

# Install required dependencies manually
python3 -m pip install django opencv-python-headless whitenoise cmake face-recognition

# Collect static files
python3 manage.py collectstatic --noinput

echo "BUILD END"
