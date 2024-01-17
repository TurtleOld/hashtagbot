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
	@poetry export -f requirements.txt --output requirements.txt --without-hashes