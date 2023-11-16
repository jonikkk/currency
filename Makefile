manage_py := ./app/manage.py


run:
	$(manage_py) runserver 0.0.0.0:8001

migrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

flake:
	flake8 app/