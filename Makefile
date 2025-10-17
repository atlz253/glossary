DOCKER_PATH = docker
DOCKER_COMPOSE_PRODUCTION = $(DOCKER_PATH)/docker-compose.production.yml
DOCKER_COMPOSE_DEVELOP = $(DOCKER_PATH)/docker-compose.develop.yml

PROTO_PATH=src/grpc/proto
PROTO_COMPILED_PATH= src/grpc/compiled

rest.start:
	fastapi run src/api/index.py --host 0.0.0.0

rest.develop:
	fastapi dev src/api/index.py --host 0.0.0.0

grpc.start:
	python -m src.grpc.index

grpc.develop:
	watchfiles "python -m src.grpc.index"

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

proto.build:
	python -m grpc_tools.protoc -I $(PROTO_PATH) --python_betterproto_out=$(PROTO_COMPILED_PATH) $(PROTO_PATH)/*.proto
