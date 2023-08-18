# exit on error
set -o errexit

pip install -r ./requirements.txt

cd $(dirname $(find . | grep manage.py$))
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --username admin --email "pabloviano13@gmail.com" --noinput || true
