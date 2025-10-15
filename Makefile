# Makefile para Seção 5.1 - Embeddings Avançados e Clustering
# Autor: Sistema de Aulas NLP
# Versão: 1.0

# Carregar variáveis de ambiente do arquivo .env se existir
# Procura primeiro na pasta raiz, depois na pasta setup/
ifneq (,$(wildcard .env))
    include .env
    export
else ifneq (,$(wildcard setup/.env))
    include setup/.env
    export
endif

# Configurações
PYTHON := python3
PIP := pip3
DOCKER := docker
DOCKER_COMPOSE := docker-compose
NOTEBOOK := Seção5.1_Embeddings.ipynb

# Cores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m # No Color

# Diretórios
SETUP_DIR := setup
DATA_DIR := data
MODELS_DIR := models
RESULTS_DIR := results
LOGS_DIR := logs

.PHONY: help install test start clean docker-up docker-down status check-env setup-dirs create-env

# Target padrão
.DEFAULT_GOAL := help

help: ## Mostra esta mensagem de ajuda
	@echo "$(CYAN)🎓 Seção 5.1 - Embeddings Avançados e Clustering$(NC)"
	@echo "$(CYAN)================================================$(NC)"
	@echo ""
	@echo "$(GREEN)Comandos disponíveis:$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BLUE)Exemplos de uso:$(NC)"
	@echo "  make install    # Instala dependências"
	@echo "  make test       # Testa o ambiente"
	@echo "  make start      # Inicia o notebook"
	@echo "  make all        # Executa tudo (install + test + start)"

all: install test start ## Executa tudo: instala, testa e inicia

install: setup-dirs ## Instala dependências Python
	@echo "$(BLUE)🔄 Instalando dependências...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install python-dotenv
	@echo "$(GREEN)✅ Dependências instaladas$(NC)"

test: ## Testa o ambiente e funcionalidades
	@echo "$(BLUE)🧪 Testando ambiente...$(NC)"
	$(PYTHON) $(SETUP_DIR)/test_environment.py
	@echo "$(GREEN)✅ Testes concluídos$(NC)"

start: ## Inicia o Jupyter Notebook
	@echo "$(BLUE)🚀 Iniciando Jupyter Notebook...$(NC)"
	$(PYTHON) $(SETUP_DIR)/start_notebook.py

setup: install test ## Configura o ambiente completo
	@echo "$(GREEN)✅ Ambiente configurado com sucesso!$(NC)"

setup-dirs: ## Cria diretórios necessários
	@echo "$(BLUE)📁 Criando diretórios...$(NC)"
	@mkdir -p $(DATA_DIR) $(MODELS_DIR) $(RESULTS_DIR) $(LOGS_DIR)
	@echo "$(GREEN)✅ Diretórios criados$(NC)"

create-env: ## Cria arquivo .env baseado no exemplo
	@echo "$(BLUE)📄 Criando arquivo .env...$(NC)"
	@if [ ! -f .env ]; then \
		if [ -f $(SETUP_DIR)/.env ]; then \
			cp $(SETUP_DIR)/.env .env; \
			echo "$(GREEN)✅ Arquivo .env copiado de setup/.env$(NC)"; \
		else \
			cp $(SETUP_DIR)/config_example.env .env; \
			echo "$(GREEN)✅ Arquivo .env criado baseado no exemplo$(NC)"; \
		fi; \
		echo "$(CYAN)💡 Edite o arquivo .env com suas configurações$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Arquivo .env já existe na pasta raiz$(NC)"; \
		echo "$(CYAN)💡 Para recriar, delete o arquivo atual e execute novamente$(NC)"; \
	fi

docker-up: ## Inicia Elasticsearch e Kibana
	@echo "$(BLUE)🐳 Iniciando Elasticsearch e Kibana...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✅ Serviços iniciados$(NC)"
	@echo "$(CYAN)📊 Kibana disponível em: http://localhost:5601$(NC)"
	@echo "$(CYAN)🔍 Elasticsearch disponível em: http://localhost:9200$(NC)"

docker-down: ## Para Elasticsearch e Kibana
	@echo "$(BLUE)🛑 Parando serviços...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Serviços parados$(NC)"

docker-restart: docker-down docker-up ## Reinicia os serviços Docker

status: ## Mostra status dos serviços
	@echo "$(BLUE)📊 Status dos serviços:$(NC)"
	@echo ""
	@echo "$(YELLOW)Python:$(NC)"
	@$(PYTHON) --version
	@echo ""
	@echo "$(YELLOW)Docker:$(NC)"
	@$(DOCKER) --version 2>/dev/null || echo "$(RED)❌ Docker não encontrado$(NC)"
	@echo ""
	@echo "$(YELLOW)Elasticsearch:$(NC)"
	@curl -s http://localhost:9200 >/dev/null 2>&1 && echo "$(GREEN)✅ Rodando$(NC)" || echo "$(RED)❌ Parado$(NC)"
	@echo ""
	@echo "$(YELLOW)Kibana:$(NC)"
	@curl -s http://localhost:5601 >/dev/null 2>&1 && echo "$(GREEN)✅ Rodando$(NC)" || echo "$(RED)❌ Parado$(NC)"

check-env: ## Verifica variáveis de ambiente
	@echo "$(BLUE)🔍 Verificando variáveis de ambiente...$(NC)"
	@echo ""
	@if [ -f .env ]; then \
		echo "$(GREEN)✅ Arquivo .env encontrado na pasta raiz$(NC)"; \
		echo "$(YELLOW)📄 Carregando variáveis do .env...$(NC)"; \
		export $$(grep -v '^#' .env | grep -v '^$$' | xargs); \
	elif [ -f setup/.env ]; then \
		echo "$(GREEN)✅ Arquivo .env encontrado na pasta setup/$(NC)"; \
		echo "$(YELLOW)📄 Carregando variáveis do setup/.env...$(NC)"; \
		export $$(grep -v '^#' setup/.env | grep -v '^$$' | xargs); \
	else \
		echo "$(YELLOW)⚠️  Arquivo .env não encontrado$(NC)"; \
		echo "$(CYAN)💡 Crie um arquivo .env baseado em setup/config_example.env$(NC)"; \
		echo "$(CYAN)💡 Ou execute: make create-env$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)OPENAI_API_KEY:$(NC)"
	@if [ -z "$$OPENAI_API_KEY" ] || [ "$$OPENAI_API_KEY" = "sk-your-openai-key-here" ]; then \
		echo "$(RED)❌ Não configurada$(NC)"; \
		echo "$(CYAN)💡 Configure no arquivo .env: OPENAI_API_KEY=sk-sua-chave-aqui$(NC)"; \
	else \
		echo "$(GREEN)✅ Configurada ($${OPENAI_API_KEY:0:10}...)$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)ELASTICSEARCH_HOST:$(NC)"
	@echo "$${ELASTICSEARCH_HOST:-localhost}"
	@echo ""
	@echo "$(YELLOW)ELASTICSEARCH_PORT:$(NC)"
	@echo "$${ELASTICSEARCH_PORT:-9200}"
	@echo ""
	@echo "$(YELLOW)OUTRAS CONFIGURAÇÕES:$(NC)"
	@echo "  DATASET_SIZE: $${DATASET_SIZE:-10000}"
	@echo "  BATCH_SIZE: $${BATCH_SIZE:-32}"
	@echo "  MAX_CLUSTERS: $${MAX_CLUSTERS:-20}"

clean: ## Limpa arquivos temporários e caches
	@echo "$(BLUE)🧹 Limpando arquivos temporários...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.log" -delete
	@echo "$(GREEN)✅ Limpeza concluída$(NC)"

clean-all: clean docker-down ## Limpa tudo incluindo containers Docker
	@echo "$(BLUE)🗑️  Removendo volumes Docker...$(NC)"
	$(DOCKER_COMPOSE) down -v
	@echo "$(GREEN)✅ Limpeza completa$(NC)"

logs: ## Mostra logs dos serviços
	@echo "$(BLUE)📋 Logs dos serviços:$(NC)"
	$(DOCKER_COMPOSE) logs

backup: ## Cria backup dos resultados
	@echo "$(BLUE)💾 Criando backup...$(NC)"
	@tar -czf backup_$(shell date +%Y%m%d_%H%M%S).tar.gz $(RESULTS_DIR) $(MODELS_DIR) $(LOGS_DIR) 2>/dev/null || true
	@echo "$(GREEN)✅ Backup criado$(NC)"

info: ## Mostra informações do projeto
	@echo "$(CYAN)📚 Seção 5.1 - Embeddings Avançados e Clustering$(NC)"
	@echo "$(CYAN)================================================$(NC)"
	@echo ""
	@echo "$(GREEN)Objetivos:$(NC)"
	@echo "  • Explorar evolução dos embeddings (Word2Vec → BERT → OpenAI)"
	@echo "  • Implementar algoritmos de clustering clássicos e modernos"
	@echo "  • Integrar com Elasticsearch para busca semântica"
	@echo "  • Criar sistema de classificação de textos personalizados"
	@echo ""
	@echo "$(GREEN)Funcionalidades:$(NC)"
	@echo "  • Embeddings: Word2Vec, BERT, Sentence-BERT, OpenAI"
	@echo "  • Clustering: K-Means, DBSCAN, HDBSCAN"
	@echo "  • Visualização: PCA, t-SNE, UMAP"
	@echo "  • Busca semântica: Elasticsearch + Kibana"
	@echo "  • Classificação: Upload de textos personalizados"
	@echo ""
	@echo "$(GREEN)Arquivos principais:$(NC)"
	@echo "  • $(NOTEBOOK) - Notebook principal"
	@echo "  • requirements.txt - Dependências Python"
	@echo "  • docker-compose.yml - Serviços Docker"
	@echo "  • setup/ - Scripts de configuração"
	@echo "  • Documentação/Documentação.md - Documentação completa"

docs: ## Mostra a documentação completa
	@echo "$(BLUE)📚 Abrindo documentação completa...$(NC)"
	@if command -v less >/dev/null 2>&1; then \
		less Documentação/Documentação.md; \
	else \
		cat Documentação/Documentação.md; \
	fi

check-issues: ## Verifica problemas críticos no projeto
	@echo "$(BLUE)🔍 Verificando problemas críticos...$(NC)"
	$(PYTHON) $(SETUP_DIR)/check_critical_issues.py

quick: setup docker-up ## Início rápido: configura e inicia serviços
	@echo "$(GREEN)🎉 Ambiente pronto! Execute 'make start' para iniciar o notebook$(NC)"

# Comandos de desenvolvimento
dev-install: ## Instala dependências de desenvolvimento
	$(PIP) install -r requirements.txt
	$(PIP) install jupyter ipykernel

dev-test: ## Executa testes de desenvolvimento
	$(PYTHON) -m pytest tests/ -v 2>/dev/null || echo "$(YELLOW)⚠️  Pytest não disponível$(NC)"

# Comandos de monitoramento
monitor: ## Monitora recursos do sistema
	@echo "$(BLUE)📊 Monitoramento de recursos:$(NC)"
	@echo "$(YELLOW)CPU e Memória:$(NC)"
	@top -l 1 | head -10
	@echo ""
	@echo "$(YELLOW)Docker:$(NC)"
	@$(DOCKER) stats --no-stream 2>/dev/null || echo "$(RED)❌ Docker não disponível$(NC)"

# Comandos de troubleshooting
troubleshoot: ## Diagnóstico de problemas
	@echo "$(BLUE)🔧 Diagnóstico de problemas:$(NC)"
	@echo ""
	@echo "$(YELLOW)1. Verificando Python:$(NC)"
	@$(PYTHON) --version
	@echo ""
	@echo "$(YELLOW)2. Verificando pip:$(NC)"
	@$(PIP) --version
	@echo ""
	@echo "$(YELLOW)3. Verificando Docker:$(NC)"
	@$(DOCKER) --version 2>/dev/null || echo "$(RED)❌ Docker não encontrado$(NC)"
	@echo ""
	@echo "$(YELLOW)4. Verificando portas:$(NC)"
	@lsof -i :8888 2>/dev/null || echo "$(GREEN)✅ Porta 8888 livre$(NC)"
	@lsof -i :9200 2>/dev/null || echo "$(GREEN)✅ Porta 9200 livre$(NC)"
	@lsof -i :5601 2>/dev/null || echo "$(GREEN)✅ Porta 5601 livre$(NC)"
