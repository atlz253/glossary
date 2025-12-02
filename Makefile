MAKE_DIR = .make

DOCKER_PATH = docker
DOCKER_COMPOSE_PRODUCTION = $(DOCKER_PATH)/docker-compose.production.yml
DOCKER_COMPOSE_DEVELOP = $(DOCKER_PATH)/docker-compose.develop.yml

PROTO_PATH=proto
PROTO_COMPILED_PATH= src/grpc/compiled

make.dir.create:
	if not exist "$(MAKE_DIR)" md "$(MAKE_DIR)"

rest.start:
	fastapi run src/api/index.py --host 0.0.0.0

rest.develop:
	fastapi dev src/api/index.py --host 0.0.0.0

grpc.start:
	python -m src.grpc.index

grpc.develop:
	watchfiles "python -m src.grpc.index"

websocket.develop:
	uvicorn src.websocket.index:app --host 0.0.0.0 --port 5000 --reload

websocket.start:
	uvicorn src.websocket.index:app --host 0.0.0.0 --port 5000

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
	docker-compose -f $(DOCKER_COMPOSE_PRODUCTION) down

proto.build:
	python -m grpc_tools.protoc -I $(PROTO_PATH) --python_betterproto_out=$(PROTO_COMPILED_PATH) $(PROTO_PATH)/*.proto

k6.rest:
	docker compose -f k6/docker/docker-compose.yml run -e TEST_FILE=/src/tests/rest.ts --service-ports --rm k6

k6.grpc:
	docker compose -f k6/docker/docker-compose.yml run -e TEST_FILE=/src/tests/grpc.ts --service-ports --rm k6

k6.websocket:
	docker compose -f k6/docker/docker-compose.yml run -e TEST_FILE=/src/tests/websocket.ts --service-ports --rm k6