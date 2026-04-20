cd /root/django-testplatform0301/backend
pip install -r requirements-linux.txt
cp task.py  /root/miniconda3/envs/pyton38/lib/python3.8/site-packages/dvadmin_celery/views/task.py
rm -rf run.log
rm -rf celery.log
nohup python manage.py runserver 0.0.0.0:8000  > run.log 2>&1 &
nohup celery -A application.celery worker -B --loglevel=info > celery.log 2>&1 &
netstat -ntlp|grep 8000