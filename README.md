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

## ✨ Funcionalidades

### 🧮 **Geração de Embeddings**
- **TF-IDF**: Método clássico baseado em frequência de termos
- **Word2Vec**: Embeddings contextuais com treinamento local
- **BERT**: Representações bidirecionais profundas
- **Sentence-BERT**: Otimizado para similaridade de sentenças
- **OpenAI**: Embeddings de última geração via API

### 🔍 **Algoritmos de Clustering**
- **K-Means**: Clustering clássico baseado em distâncias
- **DBSCAN**: Clustering baseado em densidade
- **HDBSCAN**: Clustering hierárquico robusto

### 📊 **Visualização e Análise**
- **Redução Dimensional**: PCA, t-SNE, UMAP
- **Visualizações Interativas**: Plotly com gráficos 2D/3D
- **Métricas de Avaliação**: Silhouette, ARI, NMI, Homogeneity
- **Análise Comparativa**: Benchmark entre diferentes métodos

### 🗄️ **Sistema de Cache Inteligente**
- **Elasticsearch**: Armazenamento persistente de embeddings
- **Cache Automático**: Evita reprocessamento desnecessário
- **Validação de Integridade**: Hash MD5 para verificação
- **Economia de Tempo**: 6x-12x mais rápido em execuções subsequentes

### 📈 **Análise Detalhada**
- **Estatísticas Completas**: Dimensões, densidade, normalização
- **Exemplos Práticos**: Visualização de embeddings individuais
- **Interpretação Didática**: Explicações detalhadas de cada conceito
- **Relatórios Automáticos**: Sumários comparativos e métricas

## 🛠️ Tecnologias Utilizadas

### **Core Libraries**
- **Python 3.8+**: Linguagem principal
- **NumPy**: Computação numérica
- **Pandas**: Manipulação de dados
- **Scikit-learn**: Machine learning e clustering

### **Embeddings & NLP**
- **Gensim**: Word2Vec e modelos de linguagem
- **Sentence-Transformers**: BERT e Sentence-BERT
- **OpenAI API**: Embeddings de última geração
- **Transformers**: Modelos BERT pré-treinados

### **Visualização**
- **Matplotlib**: Gráficos estáticos
- **Seaborn**: Visualizações estatísticas
- **Plotly**: Gráficos interativos
- **UMAP**: Redução dimensional não-linear

### **Clustering Avançado**
- **HDBSCAN**: Clustering hierárquico baseado em densidade
- **DBSCAN**: Clustering baseado em densidade clássico

### **Infraestrutura**
- **Elasticsearch 8.11.0**: Sistema de cache e busca
- **Kibana**: Interface de visualização do Elasticsearch
- **Docker**: Containerização dos serviços
- **Jupyter Notebook**: Ambiente interativo

### **Utilitários**
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **tqdm**: Barras de progresso
- **wordcloud**: Nuvens de palavras

## 📦 Instalação

### **Pré-requisitos**

- **Python 3.8+** (recomendado: 3.10+)
- **Git** (para clonagem do repositório)
- **Docker** e **Docker Compose** (para Elasticsearch)
- **8GB+ RAM** (recomendado para processamento completo)

### **1. Clonagem do Repositório**

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/embeddings-avancados-clustering.git

# Entre no diretório
cd embeddings-avancados-clustering
```

### **2. Criação do Ambiente Virtual**

#### **Windows (PowerShell)**
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# Se houver erro de política de execução:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **macOS/Linux**
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate
```

### **3. Instalação das Dependências**

```bash
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
cp setup/config_example.env setup/.env

# Editar configurações (opcional)
# Windows: notepad setup/.env
# macOS/Linux: nano setup/.env
```

### **5. Inicialização do Elasticsearch**

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
echo "OPENAI_API_KEY=sk-sua-chave-aqui" >> setup/.env
```

## 🚀 Execução

### **Método 1: Jupyter Notebook (Recomendado)**

```bash
# Iniciar Jupyter
jupyter notebook

# Abrir o arquivo: Seção5.1_Embeddings.ipynb
# Executar células sequencialmente
```

### **Método 2: Makefile (Automatizado)**

```bash
# Ver comandos disponíveis
make help

# Instalar dependências
make install

# Testar ambiente
make test

# Iniciar notebook
make start

# Iniciar Elasticsearch
make docker-up

# Verificar status
make status
```

### **Método 3: Execução Direta**

```bash
# Executar notebook programaticamente
jupyter nbconvert --to notebook --execute Seção5.1_Embeddings.ipynb
```

## 📊 Estrutura do Projeto

```
Embeddings_5.1/
├── 📄 README.md                          # Este arquivo
├── 📄 requirements.txt                   # Dependências Python
├── 📄 docker-compose.yml                 # Configuração Docker
├── 📄 Makefile                          # Automação de tarefas
├── 📓 Seção5.1_Embeddings.ipynb         # Notebook principal
├── 🐍 elasticsearch_manager.py           # Gerenciador de cache
├── 📁 setup/                            # Configurações e utilitários
│   ├── config_example.env               # Exemplo de configuração
│   ├── setup_environment.py             # Script de setup
│   ├── test_environment.py              # Testes do ambiente
│   ├── test_elasticsearch_cache.py      # Testes do cache
│   └── start_notebook.py                # Inicializador do notebook
├── 📁 Documentação/                     # Documentação detalhada
│   └── Documentação.md                  # Manual completo
└── 📁 .venv/                           # Ambiente virtual (criado automaticamente)
```

## 📚 Documentação

### **Documentação Completa**
- **[Documentação.md](Documentação/Documentação.md)**: Manual detalhado com conceitos teóricos, exemplos práticos e troubleshooting

### **Conceitos Principais**

#### **Embeddings de Texto**
- **TF-IDF**: Frequência de termos × Frequência inversa de documentos
- **Word2Vec**: Representações contextuais baseadas em janela deslizante
- **BERT**: Transformers bidirecionais com attention mechanism
- **Sentence-BERT**: Otimização para similaridade de sentenças
- **OpenAI**: Embeddings de última geração treinados para similaridade

#### **Algoritmos de Clustering**
- **K-Means**: Particionamento em k clusters esféricos
- **DBSCAN**: Clustering baseado em densidade com detecção de outliers
- **HDBSCAN**: Clustering hierárquico robusto com clusters de tamanhos variados

#### **Técnicas de Visualização**
- **PCA**: Redução linear preservando variância global
- **t-SNE**: Redução não-linear preservando distâncias locais
- **UMAP**: Balanceamento entre estrutura local e global

## 🔧 Configuração

### **Variáveis de Ambiente**

Crie o arquivo `setup/.env` baseado em `setup/config_example.env`:

```env
# Elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
USE_ELASTICSEARCH_CACHE=true
FORCE_REGENERATE_EMBEDDINGS=false

# OpenAI (opcional)
OPENAI_API_KEY=sk-sua-chave-aqui

# Configurações de Processamento
MAX_CHARS_PER_REQUEST=30000
BATCH_SIZE_SMALL_TEXTS=8
BATCH_SIZE_MEDIUM_TEXTS=4
BATCH_SIZE_LARGE_TEXTS=2
TEXT_MIN_LENGTH=50

# Configurações de Clustering
MAX_CLUSTERS=20
CLUSTERING_RANDOM_STATE=42

# Configurações de Visualização
PLOT_WIDTH=800
PLOT_HEIGHT=600
LOG_LEVEL=INFO
```

### **Configuração do Elasticsearch**

O Elasticsearch é configurado automaticamente via Docker Compose:

- **Porta**: 9200 (Elasticsearch), 5601 (Kibana)
- **Memória**: 1GB (configurável)
- **Segurança**: Desabilitada para ambiente educacional
- **Dados**: Persistidos em volume Docker

### **Configuração da OpenAI**

1. Obtenha uma chave API em [platform.openai.com](https://platform.openai.com)
2. Adicione a chave no arquivo `setup/.env`
3. Configure limites de uso conforme necessário

## 💡 Exemplos de Uso

### **1. Análise Básica de Embeddings**

```python
# Carregar dados
from sklearn.datasets import fetch_20newsgroups
newsgroups = fetch_20newsgroups(subset='train', categories=['sci.med', 'sci.crypt'])

# Gerar embeddings TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=1000)
embeddings = vectorizer.fit_transform(newsgroups.data)

# Aplicar clustering
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(embeddings.toarray())
```

### **2. Uso do Sistema de Cache**

```python
# Verificar cache
from elasticsearch_manager import check_embeddings_in_cache
exists, existing, missing = check_embeddings_in_cache('embeddings_tfidf', doc_ids)

# Carregar do cache
if exists:
    embeddings = load_embeddings_from_cache('embeddings_tfidf', doc_ids)
else:
    # Gerar novos embeddings
    embeddings = generate_embeddings(texts)
    save_embeddings_to_cache('embeddings_tfidf', embeddings, doc_ids, texts, 'tfidf')
```

### **3. Visualização de Resultados**

```python
# Reduzir dimensões
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
embeddings_2d = pca.fit_transform(embeddings)

# Visualizar com Plotly
import plotly.express as px
fig = px.scatter(x=embeddings_2d[:, 0], y=embeddings_2d[:, 1], 
                 color=clusters, title='Clustering Results')
fig.show()
```

## 🎓 Casos de Uso Educacionais

### **1. Comparação de Embeddings**
- Execute o notebook completo
- Compare visualizações de diferentes tipos de embeddings
- Analise métricas de qualidade

### **2. Análise de Clustering**
- Teste diferentes algoritmos de clustering
- Compare métricas de avaliação
- Identifique o melhor método para seus dados

### **3. Otimização de Performance**
- Use o sistema de cache para evitar reprocessamento
- Compare tempos de execução com/sem cache
- Analise economia de recursos

### **4. Experimentação**
- Modifique parâmetros dos algoritmos
- Teste com diferentes datasets
- Implemente novas métricas de avaliação

## 🔍 Troubleshooting

### **Problemas Comuns**

#### **Erro de Memória**
```bash
# Aumentar limite de memória do Jupyter
jupyter notebook --NotebookApp.max_buffer_size=1000000000
```

#### **Elasticsearch não conecta**
```bash
# Verificar status do Docker
docker-compose ps

# Reiniciar serviços
docker-compose restart

# Verificar logs
docker-compose logs elasticsearch
```

#### **Dependências não instalam**
```bash
# Atualizar pip
pip install --upgrade pip setuptools wheel

# Instalar com verbose
pip install -r requirements.txt -v
```

#### **OpenAI API falha**
- Verificar chave API no arquivo `.env`
- Verificar limites de uso na conta OpenAI
- Verificar conectividade com internet

### **Logs e Debug**

```bash
# Ver logs do Elasticsearch
docker-compose logs -f elasticsearch

# Testar ambiente
python setup/test_environment.py

# Testar cache
python setup/test_elasticsearch_cache.py
```

## 🤝 Contribuição

### **Como Contribuir**

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### **Áreas de Contribuição**

- **Novos tipos de embeddings**: Adicionar outros modelos
- **Algoritmos de clustering**: Implementar novos métodos
- **Visualizações**: Melhorar gráficos e interatividade
- **Documentação**: Expandir explicações e exemplos
- **Testes**: Adicionar testes automatizados
- **Performance**: Otimizar código e cache

### **Padrões de Código**

- **PEP 8**: Seguir convenções do Python
- **Docstrings**: Documentar todas as funções
- **Type Hints**: Usar anotações de tipo
- **Testes**: Escrever testes para novas funcionalidades

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### **Uso Educacional**

Este projeto foi desenvolvido especificamente para fins educacionais e pode ser usado livremente em:
- Cursos universitários
- Workshops e treinamentos
- Pesquisa acadêmica
- Projetos pessoais de aprendizado

### **Atribuição**

Se usar este projeto em suas aulas ou pesquisas, por favor cite:

```
Embeddings Avançados e Clustering Semântico
Disciplina: Inteligência Computacional para Engenharia de Produção
Universidade: [Sua Universidade]
Ano: 2025
```

## 📞 Suporte

### **Canais de Suporte**

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/embeddings-avancados-clustering/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/embeddings-avancados-clustering/discussions)
- **Email**: [seu-email@universidade.edu](mailto:seu-email@universidade.edu)

### **Recursos Adicionais**

- **Documentação Oficial**: [Documentação.md](Documentação/Documentação.md)
- **Exemplos**: Veja a pasta `examples/` (em desenvolvimento)
- **Vídeos Tutoriais**: [Canal YouTube](https://youtube.com/playlist) (em desenvolvimento)

---

<div align="center">

**🎓 Desenvolvido para fins educacionais**  
**📚 Inteligência Computacional para Engenharia de Produção**  
**🚀 2025**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/seu-usuario/embeddings-avancados-clustering)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)

</div>
