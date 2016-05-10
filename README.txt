ansible web write by flask

1. pip install -r requirements.txt
2. python manage.py init_db
3. python manage.py createsuperuser
4. python manage.py runserver
# bug: celery must gevent pool
5. celery -A app.celery worker -P gevent
6. celery -A app.celery multi start 4 -l INFO -P gevent 
