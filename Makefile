MANAGE := poetry run python manage.py

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

install:
	poetry install

start:
	@$(MANAGE) runserver
