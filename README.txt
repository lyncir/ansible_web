ansible web write by flask

1. pip install -r requirements.txt
2. python manage.py init_db
3. python manage.py createsuperuser
# bugfix: working by export PYTHONOPTIMIZE=1 https://github.com/ansible/ansible/issues/14408
4. python manage.py runserver
5. celery -A app.celery worker
6. celery -A app.celery multi start 4 -l INFO -P gevent 
7. config ansble plugins: ansible.cfg 
callback_plugins = /path/to/project/app/plugins/callback_plugins
