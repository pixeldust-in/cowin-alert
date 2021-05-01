.PHONY: help run collect deps migrate freeze
APPNAME := cowin_alert

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile


# target: run - Runs a dev server on localhost:8000
run:
	manage runserver


# target: collect - calls the "collectstatic" django command
collect:
	manage collectstatic --no-input

# target: deps - install dependencies from requirements file
deps:
	pip install -U pip setuptools
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	cd src && pip install -e .


# target: production deps - install dependencies from requirements file
prod_deps:
	pip install -U pip setuptools
	pip install -r requirements.txt
	cd src && pip install -e .


# target: migrate - migrate the database
migrate:
	manage migrate

# target: sh - open django extension's shell plus
sh:
	manage shell_plus

# target: db - open django DB shell
db:
	manage dbshell


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
