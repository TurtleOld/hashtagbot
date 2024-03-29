.env:
	@test ! -f .env && cp .env.example .env

docker-install: .env
	docker build -t gethashtag-bot .

docker-start:
	docker compose up -d

docker-stop:
	docker compose down || true

install:
	@poetry install

export-requirements:
	@poetry export -f requirements.txt -o requirements.txt --without-hashes

coverage:
	@poetry run coverage run -m pytest
	@poetry run coverage xml
	@poetry run coverage report