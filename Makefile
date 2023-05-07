SHELL := /bin/bash

PHONNY: docker_up_db
up_db:
	@docker compose up -d database

PHONNY: build
build:
	@docker compose build

PHONNY: docker_build_and_up_dev
build_and_up:
	@docker compose build
	@docker compose up -d

PHONNY: up
up:
	@docker compose up -d

PHONNY: docker_down_dev
down:
	@docker compose down

PHONNY: makemigrations
makemigrations:
	@docker compose exec backend ./manage.py makemigrations

PHONNY: migrate
migrate:
	@docker compose exec backend ./manage.py migrate

PHONNY: create_admin
create_admin:
	@docker compose exec -it backend ./manage.py createsuperuser

PHONNY: test
test:
	@docker compose run backend pytest -s -n 2

PHONNY: linter
linter:
	@docker compose exec backend pflake8
	@docker compose exec frontend npm run lint

PHONNY: fmt
fmt:
	@docker compose exec backend isort tracker
	@docker compose exec backend black tracker
