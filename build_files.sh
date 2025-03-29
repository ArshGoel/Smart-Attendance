echo "BUILD START"
python -m pip install https://github.com/sachadee/Dlib/releases/download/v19.22.99/dlib-19.22.99-cp310-cp310-win_amd64.whl
python -m pip install -r requirements.txt
python -m manage.py makemigrations 
python -m manage.py migrate
python -m manage.py makemigrations Accounts
python -m manage.py migrate Accounts
python -m manage.py makemigrations Services
python -m manage.py migrate Services
python manage.py collectstatic --noinput --clear
echo "BUILD END"