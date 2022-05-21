set dotenv-load

BACKEND_ROOT_DIR := absolute_path("backend")
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
    cp --update .env.example .env
    docker-compose build
    @just django migrate
    @just npm install

# Run arbitry npm command
npm +cmd:
	docker-compose run --rm node npm {{cmd}}

# Run arbitry django command
django +cmd:
    docker-compose run --rm backend python manage.py {{cmd}}

# Run project
up:
    docker-compose up

run-python +cmd:
	@set -e ;\
	if [ "`docker images|grep {{DJANGO_IMAGE_NAME}}`" = '' ]; then \
	    docker-compose build backend || exit $$?; \
	fi; \
	docker run -t --rm \
	-v {{BACKEND_ROOT_DIR}}:/app \
	-v {{DATA_DIR}}/pylint:/root/.cache/pylint \
	{{DJANGO_IMAGE_NAME}} {{cmd}}

# Format code
fmt:
    @just run-python black .
    @just run-python isort .

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
