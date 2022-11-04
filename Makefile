#yes, I had a plan to write some tests
test_app:
	docker-compose  -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml run web pytest

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

build:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml build

up:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml up

migrations:
	docker-compose  -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml run web python manage.py makemigrations shopplyapp

migrate:
	docker-compose  -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml run web python manage.py migrate

collect_static:
	docker-compose  -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml run web python manage.py collectstatic
