echo "BUILD START"

export PATH="/python312/bin:$PATH"
echo "Updated PATH: $PATH"

# Install dlib separately before other packages
python3 -m pip install cmake
python3 -m pip install dlib

# Install other Python dependencies
python3 -m pip install django opencv-python whitenoise face-recognition

# Collect static files
python3 manage.py collectstatic --noinput

echo "BUILD END"
