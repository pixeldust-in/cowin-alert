.PHONY: help run collect deps migrate freeze
APPNAME := cowin_alert

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile


# target: run - Runs a dev server on localhost:8000
run:
	poetry run ./src/manage.py runserver


# target: collect - calls the "collectstatic" django command
collect:
	poetry run ./src/manage.py collectstatic --no-input

# target: deps - install dependencies from requirements file
deps:
	poetry install


# target: production deps - install dependencies from requirements file
prod_deps:
	poetry install --no-dev

# target: migrate - migrate the database
migrate:
	poetry run ./src/manage.py migrate

# target: sh - open django extension's shell plus
sh:
	poetry run ./src/manage.py shell_plus

# target: db - open django DB shell
db:
	poetry run ./src/manage.py dbshell


# target: start - start the production servers
start:
	sudo supervisorctl update
	sudo supervisorctl start $(APPNAME):*
	sudo nginx -t
	sudo nginx -s reload

# target: stop - stops the production servers
stop:
	sudo supervisorctl stop $(APPNAME):*

# target: clean_restart - cleans collects and restarts the production servers
clean_restart: prod_deps migrate collect stop start


celery:
	cd src && celery -A celery_app worker -l info --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler