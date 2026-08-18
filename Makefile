.PHONY: help \
	build build-api build-llama \
	up up-api up-llama \
	down down-api down-llama \
	restart restart-api restart-llama \
	logs logs-api logs-llama \
	ps

COMPOSE_FILE := docker-compose-dev.yaml
ENV_FILE := .env


help: ## Show this help message
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'


# -----------------------------------------------------------------------------
# API
# -----------------------------------------------------------------------------

build-api: ## Build API image
	docker compose -f $(COMPOSE_FILE) build api

up-api: ## Build and start API
	docker compose -f $(COMPOSE_FILE) up --build -d api

down-api: ## Stop and remove API
	docker compose -f $(COMPOSE_FILE) down api

restart-api: ## Restart API
	docker compose -f $(COMPOSE_FILE) down api
	docker compose -f $(COMPOSE_FILE) up --build -d api

logs-api: ## Follow API logs
	docker compose -f $(COMPOSE_FILE) logs -f api


# -----------------------------------------------------------------------------
# Llama
# -----------------------------------------------------------------------------

build-llama: ## Build llama-service image
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build llama-server

up-llama: ## Start llama-service
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d llama-server

down-llama: ## Stop llama-service
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) stop llama-server

restart-llama: ## Restart llama-service
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) restart llama-server

logs-llama: ## Follow llama-service logs
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) logs -f llama-server


# -----------------------------------------------------------------------------
# All services
# -----------------------------------------------------------------------------

build: ## Build all service images
	docker compose -f $(COMPOSE_FILE) build

up: ## Build and start all services
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up --build -d

down: ## Stop and remove all services
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down

restart: ## Restart all services
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) restart

logs: ## Follow all service logs
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) logs -f

ps: ## Show all service status
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) ps