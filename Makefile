.PHONY: help install run test lint format docker-build docker-up docker-down clean

help: ## Exibe os comandos disponíveis no Makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências do projeto e de desenvolvimento via uv
	uv sync --extra dev

run: ## Executa a API localmente com hot-reload
	uv run uvicorn app.main:app --host 0.0.0.0 --port 9123 --reload

test: ## Executa todos os testes automatizados com pytest
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run pytest -v

lint: ## Executa verificação de código estático (Ruff)
	uv run ruff check .

format: ## Formata o código-fonte automaticamente (Ruff)
	uv run ruff format .

docker-build: ## Constrói a imagem Docker da API
	docker compose build

docker-up: ## Inicia o container via Docker Compose em segundo plano
	docker compose up -d

docker-down: ## Para e remove os containers em execução
	docker compose down

clean: ## Limpa arquivos temporários e caches de teste/Python
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
