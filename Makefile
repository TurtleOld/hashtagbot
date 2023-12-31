.env:
	@test ! -f .env && cp .env.example .env

docker-install: .env
	docker build -t gethashtag-bot .

docker-start:
	docker compose up -d

docker-stop:
	docker compose down || true