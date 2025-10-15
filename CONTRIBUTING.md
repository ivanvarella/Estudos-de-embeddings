# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para o projeto **Embeddings Avançados e Clustering Semântico**! Este documento fornece diretrizes e informações para contribuidores.

## 📋 Índice

- [🎯 Como Contribuir](#-como-contribuir)
- [🛠️ Configuração do Ambiente](#️-configuração-do-ambiente)
- [📝 Padrões de Código](#-padrões-de-código)
- [🧪 Testes](#-testes)
- [📚 Documentação](#-documentação)
- [🐛 Reportar Bugs](#-reportar-bugs)
- [✨ Sugerir Funcionalidades](#-sugerir-funcionalidades)
- [📋 Checklist de Pull Request](#-checklist-de-pull-request)

## 🎯 Como Contribuir

### **Tipos de Contribuição**

1. **🐛 Correção de Bugs**: Corrigir problemas existentes
2. **✨ Novas Funcionalidades**: Adicionar recursos úteis
3. **📚 Documentação**: Melhorar explicações e exemplos
4. **🧪 Testes**: Adicionar ou melhorar testes
5. **🎨 Interface**: Melhorar visualizações e UX
6. **⚡ Performance**: Otimizar código e cache
7. **🔧 Configuração**: Melhorar setup e instalação

### **Processo de Contribuição**

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie** uma branch para sua feature
4. **Faça** suas alterações
5. **Teste** suas alterações
6. **Commit** com mensagens claras
7. **Push** para sua branch
8. **Abra** um Pull Request

## 🛠️ Configuração do Ambiente

### **1. Fork e Clone**

```bash
# Fork no GitHub, depois clone
git clone https://github.com/SEU-USUARIO/embeddings-avancados-clustering.git
cd embeddings-avancados-clustering

# Adicionar upstream
git remote add upstream https://github.com/ORIGINAL-REPO/embeddings-avancados-clustering.git
```

### **2. Ambiente de Desenvolvimento**

```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Instalar dependências de desenvolvimento
pip install pytest black flake8 mypy jupyter

# Configurar pre-commit (opcional)
pip install pre-commit
pre-commit install
```

### **3. Configuração do Projeto**

```bash
# Copiar configuração
cp setup/config_example.env setup/.env

# Iniciar Elasticsearch
docker-compose up -d

# Testar ambiente
make test
```

## 📝 Padrões de Código

### **Python Style Guide**

- **PEP 8**: Seguir convenções do Python
- **Black**: Formatação automática de código
- **Flake8**: Verificação de estilo
- **MyPy**: Verificação de tipos

```bash
# Formatar código
black .

# Verificar estilo
flake8 .

# Verificar tipos
mypy .
```

### **Estrutura de Commits**

Use o padrão **Conventional Commits**:

```
tipo(escopo): descrição

corpo da mensagem (opcional)

rodapé (opcional)
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```
feat(embeddings): adicionar suporte a OpenAI GPT-4
fix(cache): corrigir problema de timeout no Elasticsearch
docs(readme): atualizar instruções de instalação
```

### **Estrutura de Arquivos**

```
projeto/
├── 📁 src/                    # Código fonte principal
├── 📁 tests/                  # Testes automatizados
├── 📁 docs/                   # Documentação adicional
├── 📁 examples/               # Exemplos de uso
├── 📁 setup/                  # Scripts de configuração
└── 📄 README.md              # Documentação principal
```

## 🧪 Testes

### **Executar Testes**

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_embeddings.py

# Com cobertura
pytest --cov=src tests/

# Testes do ambiente
python setup/test_environment.py

# Testes do cache
python setup/test_elasticsearch_cache.py
```

### **Escrever Testes**

```python
# tests/test_embeddings.py
import pytest
import numpy as np
from src.embeddings import generate_tfidf_embeddings

def test_tfidf_embeddings():
    """Testa geração de embeddings TF-IDF"""
    texts = ["Hello world", "Machine learning is great"]
    embeddings = generate_tfidf_embeddings(texts)
    
    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] > 0
    assert not np.isnan(embeddings).any()

def test_embeddings_consistency():
    """Testa consistência dos embeddings"""
    texts = ["Same text", "Same text"]
    embeddings = generate_tfidf_embeddings(texts)
    
    # Embeddings idênticos devem ser iguais
    np.testing.assert_array_almost_equal(embeddings[0], embeddings[1])
```

## 📚 Documentação

### **Documentar Código**

```python
def generate_embeddings(texts, method='tfidf', **kwargs):
    """
    Gera embeddings para uma lista de textos.
    
    Args:
        texts (List[str]): Lista de textos para processar
        method (str): Método de embedding ('tfidf', 'word2vec', 'bert')
        **kwargs: Parâmetros específicos do método
        
    Returns:
        np.ndarray: Array de embeddings com shape (n_texts, n_dimensions)
        
    Raises:
        ValueError: Se método não for suportado
        ImportError: Se dependências não estiverem instaladas
        
    Example:
        >>> texts = ["Hello world", "Machine learning"]
        >>> embeddings = generate_embeddings(texts, method='tfidf')
        >>> print(embeddings.shape)
        (2, 1000)
    """
    # Implementação...
```

### **Atualizar Documentação**

- **README.md**: Informações principais do projeto
- **Documentação.md**: Manual detalhado
- **Docstrings**: Documentação inline do código
- **Exemplos**: Scripts de exemplo em `examples/`

## 🐛 Reportar Bugs

### **Template de Bug Report**

```markdown
## 🐛 Descrição do Bug

Descrição clara e concisa do problema.

## 🔄 Passos para Reproduzir

1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

## 🎯 Comportamento Esperado

Descrição do que deveria acontecer.

## 📸 Screenshots

Se aplicável, adicione screenshots.

## 🖥️ Ambiente

- OS: [ex: Windows 10, macOS 12, Ubuntu 20.04]
- Python: [ex: 3.9.7]
- Versão do projeto: [ex: 1.0.0]

## 📋 Logs

```
Cole aqui os logs de erro
```

## 🔍 Contexto Adicional

Qualquer outra informação relevante.
```

## ✨ Sugerir Funcionalidades

### **Template de Feature Request**

```markdown
## ✨ Descrição da Funcionalidade

Descrição clara da funcionalidade desejada.

## 🎯 Problema que Resolve

Explicação do problema que esta funcionalidade resolveria.

## 💡 Solução Proposta

Descrição detalhada da solução proposta.

## 🔄 Alternativas Consideradas

Outras soluções que foram consideradas.

## 📚 Contexto Adicional

Qualquer outra informação relevante.
```

## 📋 Checklist de Pull Request

### **Antes de Submeter**

- [ ] **Código testado**: Todos os testes passam
- [ ] **Documentação atualizada**: README e docstrings atualizados
- [ ] **Estilo de código**: Black e flake8 aplicados
- [ ] **Commits organizados**: Mensagens claras e atômicas
- [ ] **Branch atualizada**: Rebase com main/develop
- [ ] **Conflitos resolvidos**: Merge conflicts resolvidos

### **Template de Pull Request**

```markdown
## 📋 Descrição

Breve descrição das alterações.

## 🔗 Issues Relacionadas

Fixes #123
Closes #456

## 🧪 Testes

- [ ] Testes unitários adicionados/atualizados
- [ ] Testes de integração executados
- [ ] Testes manuais realizados

## 📚 Documentação

- [ ] README atualizado (se necessário)
- [ ] Docstrings adicionadas/atualizadas
- [ ] Exemplos atualizados

## 🔍 Checklist de Revisão

- [ ] Código revisado por mim mesmo
- [ ] Funcionalidade testada
- [ ] Performance considerada
- [ ] Segurança verificada

## 📸 Screenshots

Se aplicável, adicione screenshots das mudanças visuais.

## 🔍 Notas para Revisores

Informações adicionais para os revisores.
```

## 🏷️ Labels e Milestones

### **Labels Disponíveis**

- `bug`: Problema no código
- `enhancement`: Nova funcionalidade
- `documentation`: Melhorias na documentação
- `good first issue`: Bom para iniciantes
- `help wanted`: Precisa de ajuda
- `priority: high`: Alta prioridade
- `priority: medium`: Média prioridade
- `priority: low`: Baixa prioridade

### **Milestones**

- `v1.1.0`: Próxima versão menor
- `v2.0.0`: Próxima versão maior
- `backlog`: Funcionalidades futuras

## 🤝 Código de Conduta

### **Nossos Compromissos**

- **Inclusivo**: Ambiente acolhedor para todos
- **Respeitoso**: Tratamento respeitoso e profissional
- **Construtivo**: Feedback construtivo e útil
- **Colaborativo**: Trabalho em equipe e cooperação

### **Comportamentos Esperados**

- ✅ Usar linguagem acolhedora e inclusiva
- ✅ Respeitar diferentes pontos de vista
- ✅ Aceitar críticas construtivas
- ✅ Focar no que é melhor para a comunidade
- ✅ Demonstrar empatia com outros membros

### **Comportamentos Inaceitáveis**

- ❌ Linguagem ou imagens sexualizadas
- ❌ Trolling, comentários insultuosos ou ataques pessoais
- ❌ Assédio público ou privado
- ❌ Publicar informações privadas sem permissão
- ❌ Outros comportamentos inadequados em ambiente profissional

## 📞 Suporte

### **Canais de Comunicação**

- **GitHub Issues**: Para bugs e feature requests
- **GitHub Discussions**: Para discussões gerais
- **Email**: [seu-email@universidade.edu](mailto:seu-email@universidade.edu)

### **Recursos Úteis**

- **Documentação**: [Documentação.md](Documentação/Documentação.md)
- **Exemplos**: [example_usage.py](example_usage.py)
- **Testes**: [setup/test_environment.py](setup/test_environment.py)

---

**Obrigado por contribuir! 🎉**

Cada contribuição, por menor que seja, ajuda a tornar este projeto melhor para toda a comunidade educacional.
