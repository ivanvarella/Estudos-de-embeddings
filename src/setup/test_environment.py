#!/usr/bin/env python3
"""
Script de teste para verificar se o ambiente está funcionando corretamente
Execute este script para testar todas as funcionalidades antes de rodar o notebook.
"""

import sys
import importlib
import numpy as np
import pandas as pd
from pathlib import Path
import os

# Suprimir warnings do tokenizers
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

def test_imports():
    """Testa se todas as dependências podem ser importadas"""
    print("🔄 Testando imports...")
    
    required_modules = [
        'numpy', 'pandas', 'matplotlib', 'seaborn', 'sklearn',
        'sentence_transformers', 'gensim', 'plotly', 'umap'
    ]
    
    optional_modules = [
        'openai', 'elasticsearch', 'hdbscan', 'streamlit', 'wordcloud'
    ]
    
    failed_imports = []
    
    # Testar módulos obrigatórios
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    # Testar módulos opcionais
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module} (opcional)")
        except ImportError:
            print(f"  ⚠️  {module} (opcional) - não instalado")
    
    return len(failed_imports) == 0

def test_sklearn_functionality():
    """Testa funcionalidades básicas do scikit-learn"""
    print("\n🔄 Testando scikit-learn...")
    
    try:
        from sklearn.datasets import fetch_20newsgroups
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        
        # Testar carregamento de dados
        newsgroups = fetch_20newsgroups(subset='train', categories=['alt.atheism'], remove=('headers', 'footers', 'quotes'))
        print(f"  ✅ Dataset carregado: {len(newsgroups.data)} documentos")
        
        # Testar clustering básico
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(max_features=100)
        X = vectorizer.fit_transform(newsgroups.data[:100])
        
        kmeans = KMeans(n_clusters=2, random_state=42)
        labels = kmeans.fit_predict(X.toarray())
        
        silhouette = silhouette_score(X.toarray(), labels)
        print(f"  ✅ Clustering testado: Silhouette = {silhouette:.3f}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no scikit-learn: {e}")
        return False

def test_sentence_transformers():
    """Testa Sentence Transformers"""
    print("\n🔄 Testando Sentence Transformers...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Carregar modelo pequeno para teste
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Testar encoding
        texts = ["This is a test sentence.", "Another test sentence."]
        embeddings = model.encode(texts)
        
        print(f"  ✅ Modelo carregado: {embeddings.shape}")
        print(f"  ✅ Embeddings gerados: {len(embeddings)} vetores")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no Sentence Transformers: {e}")
        return False

def test_gensim():
    """Testa Gensim"""
    print("\n🔄 Testando Gensim...")
    
    try:
        from gensim.models import Word2Vec
        
        # Dados de teste simples
        sentences = [["hello", "world"], ["gensim", "test"], ["word2vec", "model"]]
        
        # Treinar modelo pequeno
        model = Word2Vec(sentences, vector_size=10, window=2, min_count=1, epochs=1)
        
        print(f"  ✅ Word2Vec treinado: {len(model.wv)} palavras")
        
        # Testar similaridade
        if "hello" in model.wv and "world" in model.wv:
            similarity = model.wv.similarity("hello", "world")
            print(f"  ✅ Similaridade testada: {similarity:.3f}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no Gensim: {e}")
        return False

def test_plotly():
    """Testa Plotly"""
    print("\n🔄 Testando Plotly...")
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Criar dados de teste
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'color': np.random.randint(0, 3, 100)
        })
        
        # Testar scatter plot
        fig = px.scatter(df, x='x', y='y', color='color')
        print(f"  ✅ Gráfico criado: {len(fig.data)} traços")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no Plotly: {e}")
        return False

def test_umap():
    """Testa UMAP"""
    print("\n🔄 Testando UMAP...")
    
    try:
        import umap
        
        # Dados de teste
        data = np.random.randn(100, 10)
        
        # Reduzir dimensões
        reducer = umap.UMAP(n_components=2, random_state=42)
        embedding = reducer.fit_transform(data)
        
        print(f"  ✅ UMAP executado: {embedding.shape}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no UMAP: {e}")
        return False

def test_openai():
    """Testa OpenAI (se disponível)"""
    print("\n🔄 Testando OpenAI...")
    
    try:
        import openai
        import os
        
        # Carregar chave do .env se existir (procurar primeiro em setup/, depois na raiz)
        env_paths = [
            Path(__file__).parent / ".env",  # setup/.env
            Path(__file__).parent.parent / ".env",  # raiz/.env
        ]
        
        env_loaded = False
        for env_file in env_paths:
            if env_file.exists():
                try:
                    from dotenv import load_dotenv
                    load_dotenv(env_file)
                    env_loaded = True
                    break
                except ImportError:
                    # Se dotenv não estiver disponível, carregar manualmente
                    with open(env_file, 'r') as f:
                        for line in f:
                            if line.strip() and not line.startswith('#'):
                                if '=' in line:
                                    key, value = line.strip().split('=', 1)
                                    os.environ[key] = value
                    env_loaded = True
                    break
        
        # Verificar se a chave está configurada
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'sk-your-openai-key-here':
            print("  ⚠️  Chave da OpenAI não configurada")
            return False
        
        print("  ✅ OpenAI configurado")
        return True
    except ImportError:
        print("  ⚠️  OpenAI não instalado")
        return False
    except Exception as e:
        print(f"  ❌ Erro no OpenAI: {e}")
        return False

def test_elasticsearch():
    """Testa Elasticsearch (se disponível)"""
    print("\n🔄 Testando Elasticsearch...")
    
    try:
        from elasticsearch import Elasticsearch
        
        # Tentar conectar
        es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
        
        if es.ping():
            print("  ✅ Elasticsearch conectado")
            return True
        else:
            print("  ⚠️  Elasticsearch não está rodando")
            return False
    except ImportError:
        print("  ⚠️  Elasticsearch não instalado")
        return False
    except Exception as e:
        print(f"  ⚠️  Elasticsearch não disponível: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DO AMBIENTE - SEÇÃO 5.1")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Scikit-learn", test_sklearn_functionality),
        ("Sentence Transformers", test_sentence_transformers),
        ("Gensim", test_gensim),
        ("Plotly", test_plotly),
        ("UMAP", test_umap),
        ("OpenAI", test_openai),
        ("Elasticsearch", test_elasticsearch)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:<20}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! O ambiente está pronto.")
        print("Você pode executar o notebook com segurança.")
    elif passed >= total - 2:  # Permite 2 falhas (OpenAI e Elasticsearch são opcionais)
        print("\n✅ Ambiente funcional! Alguns recursos opcionais não estão disponíveis.")
        print("Você pode executar o notebook, mas algumas funcionalidades podem estar limitadas.")
    else:
        print("\n❌ Ambiente com problemas. Verifique as dependências antes de continuar.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
