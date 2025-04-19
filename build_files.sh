echo "BUILD START"
python3 -m pip install ./static/dlib_library/dlib-19.24.99-cp312-cp312-win_amd64.whl
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations  
python3 manage.py migrate
python3 manage.py collectstatic --noinput --clear
echo "BUILD END"
