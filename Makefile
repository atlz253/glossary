start:
	fastapi run src/index.py --host 0.0.0.0

develop:
	fastapi dev src/index.py --host 0.0.0.0

docker.develop.up:
	docker-compose -f .\docker-compose.production.yml -f .\docker-compose.develop.yml up

docker.develop.build:
	docker-compose -f .\docker-compose.production.yml -f .\docker-compose.develop.yml build

docker.production.up:
	docker-compose -f .\docker-compose.production.yml up

docker.production.build:
	docker-compose -f .\docker-compose.production.yml build