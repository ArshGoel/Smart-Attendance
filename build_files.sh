echo "BUILD START"
python3 -m pip install -r requirements.txt
pip install psycopg2-binary
python3 manage.py makemigrations  
python3 manage.py migrate
python3 manage.py collectstatic --noinput --clear
echo "BUILD END"
