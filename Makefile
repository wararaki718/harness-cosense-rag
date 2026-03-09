.PHONY: up down build logs ps clean health

# Start all services
up:
	docker compose up -d

# Stop all services
down:
	docker compose down

# Build all services
build:
	docker compose build

# Follow logs
logs:
	docker compose logs -f

# Show status
ps:
	docker compose ps

# Clean up volumes and images
clean:
	docker compose down -v --rmi local

# Health check for core services
health:
	@echo "Checking Elasticsearch... "
	@curl -s http://localhost:9200/_cluster/health | grep -q '"status":"green"\|"status":"yellow"' && echo "OK" || echo "FAILED"
	@echo "Checking SPLADE API... "
	@curl -s http://localhost:8001/ && echo "OK" || echo "FAILED"
	@echo "Checking LLM API... "
	@curl -s http://localhost:8002/ && echo "OK" || echo "FAILED"
	@echo "Checking Search API... "
	@curl -s http://localhost:8000/ && echo "OK" || echo "FAILED"
