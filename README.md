# COWIN-ALERT

## Local Dev Setup
This project uses poetry, the python package dependency manager. For local setup make sure you have poetry installed and a Python 3.9 available
```bash
make deps
```
This will create a virtual env in the project dir in a .venv directory. You can then either activate the virtual env with any of these 2 commands:
```bash
poetry shell
# OR
source .venv/bin/activate
```
If you used `poetry shell` you can do `exit` to exit the shell or just do `deactivate` to remain in that shell and just deactivate the environment.

To run your scripts either activate the virtual env or run them with poetry
```bash
poetry run ./manage.py shell_plus
```
If you want to add a package in the environment do either of these depending whether its a dev dependency or not:
```bash
poetry add requests
# OR
poetry add --dev black
```

## Create new app in the project
To create a new app in the project, do the following:
```
mkdir src/appname
poetry run ./manage.py startapp appname src/appname
```
Go to file `src/appname/apps.py` and change the attribute `MainConfig.name` from `"appname"` to `"src.appname"`.
Now you can configure the app in `INSTALLED_APPS` in settings file as `"src.appname"`