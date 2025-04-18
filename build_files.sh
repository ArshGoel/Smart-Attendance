echo "BUILD START"
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade wheel
python3 -m pip install --upgrade pipenv
python3 -m pip install --upgrade django
python3 -m pip install psycopg2-binary
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations  
python3 manage.py migrate
python3 manage.py collectstatic --noinput --clear
echo "BUILD END"
