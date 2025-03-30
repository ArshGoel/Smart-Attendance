echo "BUILD START"

# Install dependencies
# python -m pip install --upgrade pi
pip install django whitenoise opencv-python cmake face-recognition 


# Install additional dependencies from requirements.txt
# python -m pip install -r requirements.txt

# Run migrations
python manage.py makemigrations 
python manage.py migrate
python manage.py makemigrations Accounts
python manage.py migrate Accounts
python manage.py makemigrations Services
python manage.py migrate Services

# Collect static files
python manage.py collectstatic --noinput --clear

echo "BUILD END"
