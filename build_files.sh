echo "BUILD START"
# Update and install dependencies (for Debian/Ubuntu-based)
apk update && apk add build-base cmake python3-dev boost-dev

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dlib from source
python3 -m pip install dlib
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations  
python3 manage.py migrate
python3 manage.py collectstatic --noinput --clear
echo "BUILD END"
