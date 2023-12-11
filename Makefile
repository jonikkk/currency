manage_py := ./app/manage.py

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