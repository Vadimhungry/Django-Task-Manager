MANAGE := poetry run python manage.py

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

install:
	poetry install

start:
	@$(MANAGE) runserver

test:
	@$(MANAGE) test --verbosity 2

migrations:
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

lint:
	poetry run flake8 --exclude=migrations,settings.py task_manager

test-coverage:
	poetry run coverage run --source="task_manager" manage.py test task_manager
	poetry run coverage xml