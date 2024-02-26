FROM python:3.11.2

WORKDIR /project/code

ENV PYTHONPATH /project/code/app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

#CMD python ./app/manage.py runserver 0.0.0.0:8000
CMD gunicorn --workers 4 settings.wsgi --timeout 30 --max-requests 10000 --log-level info --bind 0.0.0.0:8000



