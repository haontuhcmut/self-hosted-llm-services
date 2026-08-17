.PHONY: help build up down restart logs ps

help: ## Show this help message
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

build: ## Build Docker images
	docker compose -f "docker-compose-dev.yaml" build

up: ## Build and start containers
	docker compose -f "docker-compose-dev.yaml" up --build -d

down: ## Stop and remove containers
	docker compose -f "docker-compose-dev.yaml" down

restart: ## Restart containers
	docker compose -f "docker-compose-dev.yaml" down
	docker compose -f "docker-compose-dev.yaml" up --build -d

logs: ## Follow container logs
	docker compose -f "docker-compose-dev.yaml" logs -f

ps: ## Show container status
	docker compose -f "docker-compose-dev.yaml" ps

llama-up: ## Start llama-service
	docker compose -f "docker-compose-dev.yaml" --env-file .env up -d llama-server

llama-down: ## Stop llama-service
	docker compose -f "docker-compose-dev.yaml" --env-file .env stop -d llama-server
