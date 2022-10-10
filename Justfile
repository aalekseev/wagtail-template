set dotenv-load

BACKEND_ROOT_DIR := absolute_path("backend")
FRONTEND_ROOT_DIR := absolute_path("frontend")
DATA_DIR := absolute_path(".data")
CUR_DIR_NAME := ```
basename `pwd`
```
DJANGO_IMAGE_NAME := lowercase(CUR_DIR_NAME + "_backend")

alias quality := lint

@_default:
	just --list

# Setup project
setup:
	cp --no-clobber .env.example .env
	docker-compose build
	@just django migrate
	@just yarn

# Shortcut for yarn command, i.e "just yarn add --dev prettier"
yarn *cmd:
	docker-compose run --rm frontend yarn {{cmd}}

# Shortcut for python manage.py command, i.e "just django shell"
django +cmd:
	docker-compose run --rm backend python manage.py {{cmd}}

# Bring the project up
up:
	docker-compose up

# Run any command in Python container, i.e "just run-python black ."
run-python +cmd:
	@set -e ;\
	if [ "`docker images|grep {{DJANGO_IMAGE_NAME}}`" = '' ]; then \
		docker-compose build backend || exit $$?; \
	fi; \
	docker run --tty --rm \
	-v {{BACKEND_ROOT_DIR}}:/app \
	-v {{DATA_DIR}}/pylint:/root/.cache/pylint \
	{{DJANGO_IMAGE_NAME}} {{cmd}}

# Interact with Python dependencies, i.e "just poetry add --dev mypy"
poetry +cmd:
	@just run-python poetry {{cmd}}

# Reformat codebase
fmt:
	@just run-python black .
	@just run-python isort .
	@sudo chown -R $(id -nu) {{BACKEND_ROOT_DIR}}

_black-check-all:
	@just run-python black --check --diff .

_isort-check-all:
	@just run-python isort . --check --diff

mypy:
	@just run-python mypy --show-error-codes --namespace-packages --explicit-package-bases .

prospector:
	@just run-python prospector --without-tool pep257

lint:
	@just run-python black --check --diff .
	@just run-python isort . --check --diff
	@just prospector
	@just mypy

test +cmd="":
	docker-compose run --rm backend py.test {{cmd}}

psql:
	docker-compose exec postgres psql --user dbuser --dbname projectdb

deploy branch="master":
	git push dokku {{branch}}:master

remote-logs:
	ssh dokku@$SERVER_IP logs app

remote-django *cmd:
	ssh -t dokku@$SERVER_IP run app python manage.py {{cmd}}
