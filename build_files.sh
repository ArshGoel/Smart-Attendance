echo "BUILD START"

# Install dependencies
# python -m pip install --upgrade pip
python3 -m /Django_Final/wsgi.py
# Collect static files
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
