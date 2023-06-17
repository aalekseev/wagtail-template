web: gunicorn wsgi:application --bind=0.0.0.0:5000 --workers=2
release: python manage.py migrate
