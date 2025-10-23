# 🧠 Embeddings Avançados e Clustering Semântico

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.11.0-yellow.svg)](https://elastic.co)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Projeto educacional completo** para estudo de embeddings de texto e algoritmos de clustering semântico, com sistema de cache inteligente usando Elasticsearch.

## 📋 Índice

- [🎯 Visão Geral](#-visão-geral)
- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [📦 Instalação](#-instalação)
- [🚀 Execução](#-execução)
- [📊 Estrutura do Projeto](#-estrutura-do-projeto)
- [📚 Documentação](#-documentação)
- [🔧 Configuração](#-configuração)
- [💡 Exemplos de Uso](#-exemplos-de-uso)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)

## 🎯 Visão Geral

Este projeto implementa um **sistema completo de análise de embeddings de texto** e clustering semântico, desenvolvido como material educacional para a disciplina de **Inteligência Computacional para Engenharia de Produção**.

O sistema combina **5 tipos diferentes de embeddings** (TF-IDF, Word2Vec, BERT, Sentence-BERT, OpenAI) com **3 algoritmos de clustering** (K-Means, DBSCAN, HDBSCAN) para análise semântica de textos, utilizando o dataset **20 Newsgroups** como base de dados.

### 🎓 Objetivos Educacionais

- **Compreender** a evolução dos embeddings de texto (clássicos → modernos)
- **Implementar** diferentes técnicas de representação semântica
- **Aplicar** algoritmos de clustering em dados textuais
- **Visualizar** resultados em 2D/3D com técnicas de redução dimensional
- **Comparar** performance entre diferentes abordagens
- **Utilizar** sistemas de cache para otimização de performance

### 📚 Notebooks Modulares

O projeto está organizado em **5 notebooks modulares** que devem ser executados em sequência:

1. **Part1: Preparação e Dataset** - Configuração e carregamento dos dados
2. **Part2: Embeddings Locais** - TF-IDF, Word2Vec, BERT, Sentence-BERT
3. **Part3: Embeddings OpenAI** - Embeddings de última geração
4. **Part4: Análise Comparativa** - Comparação entre todos os embeddings
5. **Part5: Clustering e ML** - Redução dimensional e clustering

## ✨ Funcionalidades

### 🔤 Embeddings Implementados

- **TF-IDF**: Representação baseada em frequência de termos
- **Word2Vec**: Embeddings contextuais clássicos (Gensim)
- **BERT**: Representações bidirecionais modernas
- **Sentence-BERT**: Otimizado para similaridade de sentenças
- **OpenAI**: Embeddings de última geração (GPT-3.5/4)

### 🎯 Algoritmos de Clustering

- **K-Means**: Clustering particional clássico
- **DBSCAN**: Clustering baseado em densidade
- **HDBSCAN**: Hierarchical DBSCAN melhorado

### 📊 Visualizações

- **PCA**: Redução dimensional linear
- **t-SNE**: Redução dimensional não-linear
- **UMAP**: Redução dimensional moderna e eficiente

### 🔍 Sistema de Cache

- **Elasticsearch**: Cache inteligente de embeddings
- **Verificação de duplicatas**: Evita reprocessamento
- **Validação de integridade**: Garante consistência dos dados
- **Scroll API**: Suporte para grandes volumes de dados (>10k docs)

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.8+**
- **Jupyter Notebook**
- **NumPy & Pandas**
- **Scikit-learn**

### Embeddings
- **Sentence Transformers**
- **Gensim (Word2Vec)**
- **OpenAI API**
- **Transformers (BERT)**

### Clustering
- **HDBSCAN**
- **Scikit-learn (K-Means, DBSCAN)**

### Visualização
- **Matplotlib & Seaborn**
- **Plotly**
- **UMAP**

### Cache & Storage
- **Elasticsearch 8.11.0**
- **Kibana**

## 📦 Instalação

### **Pré-requisitos**

- Python 3.8 ou superior
- Docker Desktop (para Elasticsearch)
- Git

### **1. Clone o Repositório**

```bash
git clone <repository-url>
cd Embeddings_5.1
```

### **2. Instalação do Docker Desktop**

#### Windows
1. Baixe o [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/)
2. Execute o instalador e siga as instruções
3. Reinicie o computador se necessário

#### macOS
1. Baixe o [Docker Desktop para Mac](https://www.docker.com/products/docker-desktop/)
2. Arraste o aplicativo para a pasta Applications
3. Execute o Docker Desktop

#### Linux (Ubuntu/Debian)
```bash
# Atualizar pacotes
sudo apt update

# Instalar dependências
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# Adicionar chave GPG oficial do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Adicionar repositório Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
```

### **3. Configuração do Ambiente Python**

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
python -c "import numpy, pandas, sklearn; print('✅ Dependências instaladas!')"
```

### **4. Configuração do Ambiente**

```bash
# Copiar arquivo de configuração
cp src/setup/config_example.env src/setup/.env

# Editar configurações (opcional)
# Windows: notepad src/setup/.env
# macOS/Linux: nano src/setup/.env
```

### **5. Inicialização do Elasticsearch**

#### Windows/Linux
```bash
# Iniciar serviços Docker
docker-compose -f docker-compose-win.yml up -d

# Verificar status
docker-compose -f docker-compose-win.yml ps

# Verificar Elasticsearch
curl http://localhost:9200
```

#### macOS
```bash
# Iniciar serviços Docker
docker-compose up -d

# Verificar status
docker-compose ps

# Verificar Elasticsearch
curl http://localhost:9200
```

### **6. Configuração da API OpenAI (Opcional)**

Para usar embeddings da OpenAI, configure sua chave API:

```bash
# Editar arquivo .env
echo "OPENAI_API_KEY=sk-sua-chave-aqui" >> src/setup/.env
```

## 🚀 Execução

### **Método 1: Jupyter Notebook (Recomendado)**

```bash
# Ativar ambiente virtual
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Iniciar Jupyter
jupyter notebook src/

# Executar notebooks em sequência:
# 1. Seção5.1_Part1_Preparacao_Dataset.ipynb
# 2. Seção5.1_Part2_Embeddings_Locais.ipynb
# 3. Seção5.1_Part3_Embeddings_OpenAI.ipynb
# 4. Seção5.1_Part4_Analise_Comparativa.ipynb
# 5. Seção5.1_Part5_Clustering_ML.ipynb
```

### **Método 2: Makefile (Automatizado)**

```bash
# Ver comandos disponíveis
make help

# Instalar dependências
make install

# Testar ambiente
make test

# Iniciar Elasticsearch
make docker-up

# Iniciar Jupyter
make start

# Verificar status
make status
```

### **Método 3: Scripts Individuais**

```bash
# Configurar ambiente
python src/setup/setup_environment.py

# Testar funcionalidades
python src/setup/test_environment.py

# Iniciar Jupyter
python src/setup/start_notebook.py
```

## 📊 Estrutura do Projeto

```
Embeddings_5.1/
├── 📁 src/                           # Código fonte principal
│   ├── 📓 Seção5.1_Part1_Preparacao_Dataset.ipynb
│   ├── 📓 Seção5.1_Part2_Embeddings_Locais.ipynb
│   ├── 📓 Seção5.1_Part3_Embeddings_OpenAI.ipynb
│   ├── 📓 Seção5.1_Part4_Analise_Comparativa.ipynb
│   ├── 📓 Seção5.1_Part5_Clustering_ML.ipynb
│   ├── 🔧 elasticsearch_manager.py   # Gerenciador de cache
│   ├── 🔧 elasticsearch_helpers.py   # Funções auxiliares
│   └── 📁 setup/                     # Scripts de configuração
│       ├── ⚙️  config_example.env    # Configurações de exemplo
│       ├── 🔧 setup_environment.py   # Configuração do ambiente
│       ├── 🧪 test_environment.py    # Testes de funcionalidades
│       ├── 🚀 start_notebook.py      # Inicialização do Jupyter
│       ├── 📄 generate_pdf.py        # Geração de PDFs
│       └── 🧪 test_elasticsearch_cache.py
├── 🐳 docker-compose.yml             # Serviços Docker (macOS)
├── 🐳 docker-compose-win.yml         # Serviços Docker (Windows/Linux)
├── ⚙️  Makefile                      # Automação de comandos
├── 📋 requirements.txt               # Dependências Python
├── 📁 Documentação/                  # Documentação completa
│   └── 📄 Documentação.md
├── 📁 database/                      # Dados do Elasticsearch
└── 📄 README.md                      # Este arquivo
```

## 📚 Documentação

### **Documentação Completa**
- **Arquivo**: `Documentação/Documentação.md`
- **Conteúdo**: Guia completo de uso e configuração
- **Acesso**: `make docs` ou abrir diretamente

### **Comandos de Acesso**
```bash
make docs          # Visualiza documentação no terminal
make help          # Lista todos os comandos
make info          # Informações do projeto
```

## 🔧 Configuração

### **Variáveis de Ambiente**

O projeto usa um arquivo `.env` para configurações. Copie `src/setup/config_example.env` para `src/setup/.env` e configure:

```env
# OpenAI API (opcional)
OPENAI_API_KEY=sk-sua-chave-aqui

# Elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Configurações do dataset
DATASET_SIZE=20000
TEXT_MIN_LENGTH=20

# Configurações de clustering
MAX_CLUSTERS=20
CLUSTERING_RANDOM_STATE=42
```

### **Configurações Avançadas**

- **Processamento de textos**: `MAX_CHARS_PER_REQUEST`
- **Batch sizes**: `BATCH_SIZE_SMALL_TEXTS`, `BATCH_SIZE_MEDIUM_TEXTS`
- **Visualização**: `PLOT_WIDTH`, `PLOT_HEIGHT`
- **Cache**: `USE_ELASTICSEARCH_CACHE`, `FORCE_REGENERATE_EMBEDDINGS`

## 💡 Exemplos de Uso

### **Execução Básica**

```bash
# 1. Configurar ambiente
make install
make docker-up

# 2. Executar notebooks
make start

# 3. No Jupyter, executar em ordem:
#    Part1 → Part2 → Part3 → Part4 → Part5
```

### **Execução com OpenAI**

```bash
# 1. Configurar chave OpenAI
echo "OPENAI_API_KEY=sk-sua-chave-aqui" >> src/setup/.env

# 2. Executar normalmente
make start
```

### **Geração de PDFs**

```bash
# Gerar PDFs de todos os notebooks
python src/setup/generate_pdf.py --notebook src/

# Gerar PDF de notebook específico
python src/setup/generate_pdf.py --notebook src/Seção5.1_Part1_Preparacao_Dataset.ipynb
```

### **Limpeza e Reset**

```bash
# Limpar cache do Elasticsearch
make clean-all

# Parar serviços
make docker-down

# Limpar arquivos temporários
make clean
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**🎓 Aproveite a aula!** Este projeto oferece uma experiência completa de embeddings e clustering modernos.

**📧 Contato**: Para dúvidas ou sugestões, abra uma issue no repositório.

---

_Última atualização: 2025-01-27_
_Versão: 2.0 - Estrutura Modular_