# Makefile para Seção 5.1 - Embeddings Avançados e Clustering
# Suporte para 5 notebooks modulares
# Autor: Sistema de Aulas NLP
# Versão: 2.0

# Carregar variáveis de ambiente do arquivo .env se existir
ifneq (,$(wildcard .env))
    include .env
    export
else ifneq (,$(wildcard setup/.env))
    include setup/.env
    export
endif

# Configurações
PYTHON := python
PIP := pip3
DOCKER := docker
DOCKER_COMPOSE := docker-compose

# Cores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
CYAN := \033[0;36m
NC := \033[0m # No Color

# Diretórios
SETUP_DIR := src/setup
NOTEBOOKS_DIR := src

.PHONY: help install test start clean docker-up docker-down status check-env setup-dirs pdf pdf-exec pdf-single html pdf-both

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
	@echo "$(BLUE)Notebooks disponíveis:$(NC)"
	@echo "  Part1: Preparação e Dataset"
	@echo "  Part2: Embeddings Locais"
	@echo "  Part3: Embeddings OpenAI"
	@echo "  Part4: Análise Comparativa"
	@echo "  Part5: Clustering e ML"

all: install test docker-up ## Executa tudo: instala, testa e inicia serviços

install: setup-dirs ## Instala dependências Python
	@echo "$(BLUE)🔄 Instalando dependências...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependências instaladas$(NC)"

test: ## Testa o ambiente e funcionalidades
	@echo "$(BLUE)🧪 Testando ambiente...$(NC)"
	$(PYTHON) $(SETUP_DIR)/test_environment.py
	@echo "$(GREEN)✅ Testes concluídos$(NC)"

start: ## Inicia o Jupyter Notebook
	@echo "$(BLUE)🚀 Iniciando Jupyter Notebook...$(NC)"
	@echo "$(CYAN)📚 Notebooks disponíveis:$(NC)"
	@echo "  • Part1: Preparação e Dataset"
	@echo "  • Part2: Embeddings Locais"
	@echo "  • Part3: Embeddings OpenAI"
	@echo "  • Part4: Análise Comparativa"
	@echo "  • Part5: Clustering e ML"
	@echo ""
	@echo "$(YELLOW)💡 Execute os notebooks em ordem sequencial!$(NC)"
	jupyter notebook $(NOTEBOOKS_DIR)/

setup: install test ## Configura o ambiente completo
	@echo "$(GREEN)✅ Ambiente configurado com sucesso!$(NC)"

setup-dirs: ## Cria diretórios necessários
	@echo "$(BLUE)📁 Criando diretórios...$(NC)"
	@mkdir -p data models results logs
	@echo "$(GREEN)✅ Diretórios criados$(NC)"

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
	@if [ -f src/setup/.env ]; then \
		echo "$(GREEN)✅ Arquivo .env encontrado na pasta src/setup/$(NC)"; \
	elif [ -f .env ]; then \
		echo "$(GREEN)✅ Arquivo .env encontrado na pasta raiz$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Arquivo .env não encontrado$(NC)"; \
		echo "$(CYAN)💡 Crie um arquivo .env baseado em src/setup/config_example.env$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)OPENAI_API_KEY:$(NC)"
	@if [ -z "$$OPENAI_API_KEY" ] || [ "$$OPENAI_API_KEY" = "sk-your-openai-key-here" ]; then \
		echo "$(RED)❌ Não configurada$(NC)"; \
		echo "$(CYAN)💡 Configure no arquivo .env: OPENAI_API_KEY=sk-sua-chave-aqui$(NC)"; \
	else \
		echo "$(GREEN)✅ Configurada ($${OPENAI_API_KEY:0:10}...)$(NC)"; \
	fi

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
	@echo "$(GREEN)Notebooks:$(NC)"
	@echo "  • Part1: Preparação e Dataset"
	@echo "  • Part2: Embeddings Locais (TF-IDF, Word2Vec, BERT, Sentence-BERT)"
	@echo "  • Part3: Embeddings OpenAI"
	@echo "  • Part4: Análise Comparativa"
	@echo "  • Part5: Clustering e Machine Learning"
	@echo ""
	@echo "$(GREEN)Funcionalidades:$(NC)"
	@echo "  • Embeddings: Word2Vec, BERT, Sentence-BERT, OpenAI"
	@echo "  • Clustering: K-Means, DBSCAN, HDBSCAN"
	@echo "  • Visualização: PCA, t-SNE, UMAP"
	@echo "  • Busca semântica: Elasticsearch + Kibana"
	@echo "  • Classificação: Upload de textos personalizados"

# Comandos específicos para notebooks
notebook1: ## Abre o Notebook 1 (Preparação e Dataset)
	@echo "$(BLUE)📓 Abrindo Notebook 1: Preparação e Dataset$(NC)"
	jupyter notebook $(NOTEBOOKS_DIR)/Seção5.1_Part1_Preparacao_Dataset.ipynb

notebook2: ## Abre o Notebook 2 (Embeddings Locais)
	@echo "$(BLUE)📓 Abrindo Notebook 2: Embeddings Locais$(NC)"
	jupyter notebook $(NOTEBOOKS_DIR)/Seção5.1_Part2_Embeddings_Locais.ipynb

notebook3: ## Abre o Notebook 3 (Embeddings OpenAI)
	@echo "$(BLUE)📓 Abrindo Notebook 3: Embeddings OpenAI$(NC)"
	jupyter notebook $(NOTEBOOKS_DIR)/Seção5.1_Part3_Embeddings_OpenAI.ipynb

notebook4: ## Abre o Notebook 4 (Análise Comparativa)
	@echo "$(BLUE)📓 Abrindo Notebook 4: Análise Comparativa$(NC)"
	jupyter notebook $(NOTEBOOKS_DIR)/Seção5.1_Part4_Analise_Comparativa.ipynb

notebook5: ## Abre o Notebook 5 (Clustering e ML)
	@echo "$(BLUE)📓 Abrindo Notebook 5: Clustering e ML$(NC)"
	jupyter notebook $(NOTEBOOKS_DIR)/Seção5.1_Part5_Clustering_ML.ipynb

# Comandos de desenvolvimento
dev-install: ## Instala dependências de desenvolvimento
	$(PIP) install -r requirements.txt
	$(PIP) install jupyter ipykernel

# Comandos de geração de PDF
pdf: ## Gera PDF de todos os notebooks (sem executar células)
	@echo "$(BLUE)📄 Gerando PDFs de todos os notebooks...$(NC)"
	@echo "$(YELLOW)⚠️  Isso pode demorar alguns minutos...$(NC)"
	python $(SETUP_DIR)/generate_pdf.py --notebook $(NOTEBOOKS_DIR)/ --output results/ --no-execute
	@echo "$(GREEN)✅ PDFs gerados em results/$(NC)"

pdf-exec: ## Gera PDF de todos os notebooks (executando células)
	@echo "$(BLUE)📄 Gerando PDFs com execução de células...$(NC)"
	@echo "$(YELLOW)⚠️  Isso pode demorar MUITO tempo (30+ minutos)...$(NC)"
	python $(SETUP_DIR)/generate_pdf.py --notebook $(NOTEBOOKS_DIR)/ --output results/ --timeout 3600
	@echo "$(GREEN)✅ PDFs gerados em results/$(NC)"

pdf-single: ## Gera PDF de um notebook específico (use: make pdf-single NOTEBOOK=Part1)
	@echo "$(BLUE)📄 Gerando PDF do notebook $(NOTEBOOK)...$(NC)"
	python $(SETUP_DIR)/generate_pdf.py --notebook $(NOTEBOOKS_DIR)/Seção5.1_$(NOTEBOOK).ipynb --output results/ --no-execute
	@echo "$(GREEN)✅ PDF gerado em results/$(NC)"

html: ## Gera HTML de todos os notebooks
	@echo "$(BLUE)🌐 Gerando HTMLs de todos os notebooks...$(NC)"
	python $(SETUP_DIR)/generate_pdf.py --notebook $(NOTEBOOKS_DIR)/ --output results/ --html --no-execute
	@echo "$(GREEN)✅ HTMLs gerados em results/$(NC)"

pdf-both: ## Gera tanto PDF quanto HTML de todos os notebooks
	@echo "$(BLUE)📄🌐 Gerando PDFs e HTMLs de todos os notebooks...$(NC)"
	python $(SETUP_DIR)/generate_pdf.py --notebook $(NOTEBOOKS_DIR)/ --output results/ --both --no-execute
	@echo "$(GREEN)✅ PDFs e HTMLs gerados em results/$(NC)"

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