DOCKER_PATH = docker
DOCKER_COMPOSE_PRODUCTION = $(DOCKER_PATH)/docker-compose.production.yml
DOCKER_COMPOSE_DEVELOP = $(DOCKER_PATH)/docker-compose.develop.yml

start:
	fastapi run src/index.py --host 0.0.0.0

develop:
	fastapi dev src/index.py --host 0.0.0.0

docker.develop.up:
	docker-compose -f $(DOCKER_COMPOSE_PRODUCTION) -f $(DOCKER_COMPOSE_DEVELOP) up

docker.develop.build:
	docker-compose -f $(DOCKER_COMPOSE_PRODUCTION) -f $(DOCKER_COMPOSE_DEVELOP) build

docker.develop.down:
	docker-compose -f $(DOCKER_COMPOSE_PRODUCTION) -f $(DOCKER_COMPOSE_DEVELOP) down

docker.production.up:
	docker-compose -f $(DOCKER_COMPOSE_PRODUCTION) up

docker.production.build:
	docker-compose -f $(DOCKER_COMPOSE_PRODUCTION) build

docker.production.down:
	docker-compose -f $(DOCKER_COMPOSE_PRODUCTION) build