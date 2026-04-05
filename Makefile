PROJECT_NAME=coilcast
DOCKER_COMPOSE=docker-compose.yaml

python-venv:
	@echo "Creating virtual environment for $(PROJECT_NAME)..."
	virtualenv venv && . venv/bin/activate && pip install -r requirements.txt

.PHONY: run
run:
	@echo "Running $(PROJECT_NAME)..."
	python src/main.py

.PHONY: docker
docker:
	@echo "Building docker image for $(PROJECT_NAME)..."
	docker build -f Dockerfile -t $(PROJECT_NAME):latest .

.PHONY: up
up: docker
	@echo "Building docker container for $(PROJECT_NAME)..."
	docker-compose -f $(DOCKER_COMPOSE) up -d

.PHONY: stop
stop:
	@echo "Stopping docker container for $(PROJECT_NAME)..."
	docker-compose -f $(DOCKER_COMPOSE) stop

.PHONY: down
down:
	docker-compose -f $(DOCKER_COMPOSE) down

.PHONY: logs
logs:
	docker-compose -f $(DOCKER_COMPOSE) logs -f
