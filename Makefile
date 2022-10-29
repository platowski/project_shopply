install_app:
	python3 -m venv venv && . venv/bin/activate && poetry install

test_app:
	docker-compose  -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml run web pytest

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

build:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml build

up:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.local-overrides.yml up



