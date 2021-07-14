.PHONY: all prepare-dev remove-env install-dep clean docker
SHELL=/bin/bash

VENV_NAME?=venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_BIN}/activate

PYTHON=${VENV_BIN}/python3

venv: $(VENV_NAME)/bin/activate

install-dep:
	pip install --upgrade pip
	pip install --upgrade -r requirements/prod.txt
	pip freeze > requirements.txt

install-psycopg2:
	env LDFLAGS='-L/usr/local/lib -L/usr/local/opt/openssl/lib -L/usr/local/opt/readline/lib' pip install psycopg2



clean:
	find . -name '*.pyc' -exec rm --force {} +
	rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .cache

docker:
	COMPOSE_FILE=docker/docker-compose.yml docker-compose up --no-deps --build