set dotenv-load

PROJECT_DIR := justfile_directory()
PROJECT_NAME := replace_regex(PROJECT_DIR, ".*/", "")
BACKEND_ROOT_DIR := absolute_path("backend")
FRONTEND_ROOT_DIR := absolute_path("frontend")
DATA_DIR := absolute_path(".data")
CACHE_DIR := absolute_path(".data/pycache")
DPT_PIP_CACHE_DIR := env_var_or_default("DPT_PIP_CACHE_DIR", absolute_path(".data/pycache/pip"))
DPT_POETRY_CACHE_DIR := env_var_or_default("DPT_POETRY_CACHE_DIR", absolute_path(".data/pycache/pypoetry"))
DJANGO_IMAGE_NAME := env_var_or_default("DJANGO_IMAGE_NAME", lowercase(PROJECT_NAME + "-backend"))
NODE_IMAGE_NAME := env_var_or_default("NODE_IMAGE_NAME", lowercase(PROJECT_NAME + "-frontend"))

alias quality := lint

@_default:
	just --list

# Run this as a first command when cloned this project
setup:
	cp --no-clobber .env.example .env
	git submodule update --init --recursive
	docker compose build
	# --noinput here due to
	# https://github.com/infoportugal/wagtail-modeltranslation/issues/175
	@just django migrate --noinput
	@just yarn

# Shortcut for yarn command, i.e "just yarn add --dev prettier"
yarn *cmd:
	docker-compose run --rm frontend yarn {{cmd}}

# Shortcut for python manage.py command, i.e "just django shell"
django *cmd:
	docker compose run --rm backend python manage.py {{cmd}}

# Bring the project up
up:
	docker compose up

# Run any command in Python container, i.e "just run-python black ."
run-python +cmd:
	#!/usr/bin/env bash
	set -e
	if [ "`docker images|grep {{DJANGO_IMAGE_NAME}}`" = '' ];
	then docker compose build backend || exit 1
	fi
	docker run --tty --rm \
	-v {{BACKEND_ROOT_DIR}}:/app \
	-v {{DATA_DIR}}/pylint:/root/.cache/pylint \
	-v {{DPT_PIP_CACHE_DIR}}:/root/.cache/pip \
	-v {{DPT_POETRY_CACHE_DIR}}:/root/.cache/pypoetry \
	-v {{CACHE_DIR}}/ruff:/root/.cache/ruff \
	-v {{CACHE_DIR}}/mypy:/root/.cache/mypy \
	{{DJANGO_IMAGE_NAME}} {{cmd}}

# Interact with Python dependencies, i.e "just poetry add --dev mypy"
poetry +cmd:
	@just run-python poetry {{cmd}}
	docker compose build backend

# Reformat codebase
fmt:
	@just run-python black .
	@just run-python isort .
	@sudo chown -R $(id -nu) {{BACKEND_ROOT_DIR}}

# Check Python static types
mypy:
	@just run-python mypy --show-error-codes --namespace-packages --explicit-package-bases .

# Lint codebase
lint:
	@echo "Running formatting checks..."
	@just run-python black --check --diff .
	@just run-python isort --check --diff .
	@echo "Running code static analysis..."
	@just run-python ruff .
	@echo "Running static type checks..."
	@just mypy

# Run security audit on project dependencies
audit:
	# GHSA-2p9h-ccw7-33gf - No fix currently, limited effect on production environment
	#   (attacker needs to be able to invoke pip with custom svn repo)
	@just run-python pip-audit --fix --dry-run --desc --ignore-vuln GHSA-2p9h-ccw7-33gf

# Run python tests, i.e "just test" or "just test /app/tests/test_smth.py"
test +cmd="":
	docker compose run --rm backend py.test {{cmd}}
