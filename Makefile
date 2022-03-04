BACKEND_DIR_NAME ?= backend
# Get root dir and project dir
PROJECT_ROOT ?= $(CURDIR)
BACKEND_ROOT_DIR ?= $(PROJECT_ROOT)/$(BACKEND_DIR_NAME)
CUR_DIR_NAME ?= $(shell basename `pwd`)
DJANGO_IMAGE_NAME ?= $(CUR_DIR_NAME)_backend


.PHONY:
all: help


.PHONY:
help:
	@echo "+------<<<<                                 Configuration                                >>>>------+"
	@echo ""
	@echo "PROJECT_ROOT: $(PROJECT_ROOT)"
	@echo "SITE_ROOT: $(SITE_ROOT)"
	@echo "CUR_DIR_NAME: $(CUR_DIR_NAME)"
	@echo "DJANGO_IMAGE_NAME: $(DJANGO_IMAGE_NAME)"
	@echo ""
	@echo "+------<<<<                                     Tasks                                    >>>>------+"
	@echo ""
	@grep --no-filename -E '^[a-zA-Z_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""


.PHONY:
setup: ## Sets up the project in your local machine
	@echo "Creating Docker images"
	@docker-compose build
	@echo "Running django migrations"
	@make migrate
	@echo "===================================================================="
	@echo "SETUP SUCCEEDED"


.PHONY:
docker-manage:  ## Run management command. For example make docker-manage cmd=createsuperuser
	docker-compose run --rm backend ./manage.py $(cmd)


.PHONY:
shell:  ## Drop into Django shell
	docker-compose run --rm backend ./manage.py shell


.PHONY:
makemigrations migrations:  ## Generate new DB migrations
	docker-compose run --rm backend ./manage.py makemigrations $(cmd)


.PHONY:
migrate:  ## Apply DB migrations
	docker-compose run --rm backend ./manage.py migrate $(cmd)


# NOTE:
# Do not use `docker-compose run` to avoid spawning services by the django container
.PHONY:
run-python:
	@set -e ;\
	if [ "`docker images|grep $(DJANGO_IMAGE_NAME)`" = '' ]; then \
	    docker-compose build backend || exit $$?; \
	fi; \
	docker run -t --rm -v $(BACKEND_ROOT_DIR):/app $(DJANGO_IMAGE_NAME) $(cmd)


.PHONY:
black-check:
	@make run-python cmd="black --check --diff $(cmd)"


.PHONY:
black-check-all:
	@make run-python cmd="black --check --diff ."


.PHONY:
black-format:
	@make run-python cmd="black $(cmd)"


.PHONY:
black-format-all:
	@make run-python cmd="black ."


.PHONY:
lint: black-check-all isort python-lint mypy


.PHONY:
quality: lint ## Run quality checks


.PHONY:
fmt: black-format-all isort-fix ## Format Python Files


.PHONY:
python-lint:
	@echo "Running pylint"
	@make run-python cmd="pylint app"


.PHONY:
mypy:
	@echo "Checking types"
	@make run-python cmd="mypy --show-error-codes ."


.PHONY:
isort:
	@echo "Checking imports with isort"
	@make run-python cmd='isort . --check --diff'


.PHONY:
isort-fix:
	@echo "Fixing imports with isort"
	@make run-python cmd='isort .'


.PHONY:
test:  ## Run python test suit
	@echo "Running automatic tests"
	@docker-compose run --rm backend py.test
