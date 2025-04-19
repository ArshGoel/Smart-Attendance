echo "BUILD START"
# Update and install dependencies (for Debian/Ubuntu-based)
apt-get update && apt-get install -y build-essential cmake python3-dev libboost-all-dev

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dlib from source
python3 -m pip install dlib
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations  
python3 manage.py migrate
python3 manage.py collectstatic --noinput --clear
echo "BUILD END"
