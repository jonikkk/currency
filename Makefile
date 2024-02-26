#manage_py := ./app/manage.py
manage_py := docker compose exec -it backend python ./app/manage.py

shell:
	$(manage_py) shell_plus --print-sql

createsuperuser:
	$(manage_py) createsuperuser


run:
	$(manage_py) runserver 0.0.0.0:8001

migrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

flake:
	flake8 app/

worker:
	cd app && celery -A settings worker -l info --autoscale=0,8

beat:
	cd app && celery -A settings beat -l info

pytest:
	pytest app/tests --cov=app --cov-report html && coverage report --fail-under=75.4477

gunicorn:
	cd app && gunicorn --workers 4 settings.wsgi --timeout 30 --max-requests 10000 --log-level debug --bind 0.0.0.0:8002

collectstatic:
	$(manage_py) collectstatic --no-input && \
	docker cp backend:/tmp/static /tmp/static && \
	docker cp /tmp/static nginx:/etc/nginx/static

