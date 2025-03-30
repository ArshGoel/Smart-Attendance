echo "BUILD START"

# Update package lists
apt-get update

# Install dependencies for dlib
apt-get install -y cmake g++ make python3-dev

# Upgrade pip
python3 -m pip install --upgrade pip

# Manually install dlib before other packages
python3 -m pip install cmake
python3 -m pip install dlib

# Install other Python dependencies
python3 -m pip install django opencv-python whitenoise face-recognition

# Collect static files
python3 manage.py collectstatic --noinput

echo "BUILD END"
