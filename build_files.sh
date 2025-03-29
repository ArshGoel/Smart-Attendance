echo "BUILD START"

# Install dependencies
python -m pip install --upgrade pip
python -m pip install --no-cache-dir opencv-python face_recognition dlib

# Install additional dependencies from requirements.txt
python -m pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --clear

echo "BUILD END"
