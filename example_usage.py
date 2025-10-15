#!/usr/bin/env python3
"""
Exemplo de Uso - Embeddings Avançados e Clustering Semântico
============================================================

Este script demonstra como usar as funcionalidades principais do projeto
de forma programática, sem necessidade do Jupyter Notebook.

Autor: Sistema de Aulas NLP
Data: 2025
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configurar warnings
warnings.filterwarnings('ignore')

def main():
    """Função principal de exemplo"""
    print("🚀 EXEMPLO DE USO - EMBEDDINGS AVANÇADOS E CLUSTERING")
    print("=" * 60)
    
    # Verificar se o ambiente está configurado
    if not check_environment():
        print("❌ Ambiente não configurado corretamente")
        print("💡 Execute: make install && make test")
        return
    
    # Exemplo 1: Análise básica com TF-IDF
    print("\n📊 EXEMPLO 1: Análise Básica com TF-IDF")
    print("-" * 40)
    example_tfidf_analysis()
    
    # Exemplo 2: Uso do sistema de cache
    print("\n🗄️ EXEMPLO 2: Sistema de Cache Elasticsearch")
    print("-" * 40)
    example_cache_usage()
    
    # Exemplo 3: Clustering básico
    print("\n🔍 EXEMPLO 3: Clustering Básico")
    print("-" * 40)
    example_clustering()
    
    print("\n✅ Exemplos concluídos com sucesso!")
    print("💡 Para análise completa, use o Jupyter Notebook: Seção5.1_Embeddings.ipynb")

def check_environment():
    """Verifica se o ambiente está configurado"""
    try:
        import numpy as np
        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        print("✅ Dependências básicas disponíveis")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def example_tfidf_analysis():
    """Exemplo de análise com TF-IDF"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.datasets import fetch_20newsgroups
    
    # Carregar dados de exemplo
    print("📥 Carregando dados de exemplo...")
    newsgroups = fetch_20newsgroups(
        subset='train', 
        categories=['sci.med', 'sci.crypt'],
        remove=('headers', 'footers', 'quotes')
    )
    
    # Limitar a 100 documentos para exemplo rápido
    texts = newsgroups.data[:100]
    categories = newsgroups.target[:100]
    
    print(f"📊 Documentos carregados: {len(texts)}")
    print(f"📊 Categorias: {len(set(categories))}")
    
    # Gerar embeddings TF-IDF
    print("🔄 Gerando embeddings TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        min_df=2,
        max_df=0.8
    )
    
    embeddings = vectorizer.fit_transform(texts)
    print(f"📐 Dimensões dos embeddings: {embeddings.shape}")
    print(f"📊 Densidade: {(embeddings != 0).mean():.3f}")
    
    # Análise básica
    feature_names = vectorizer.get_feature_names_out()
    mean_tfidf = embeddings.mean(axis=0).A1
    top_features = np.argsort(mean_tfidf)[-10:][::-1]
    
    print("🔝 Top 10 features mais importantes:")
    for i, idx in enumerate(top_features):
        print(f"   {i+1:2d}. {feature_names[idx]:<15}: {mean_tfidf[idx]:.4f}")

def example_cache_usage():
    """Exemplo de uso do sistema de cache"""
    try:
        from elasticsearch_manager import (
            init_elasticsearch_cache, 
            get_cache_status,
            check_embeddings_in_cache
        )
        
        # Inicializar cache
        print("🔌 Conectando ao Elasticsearch...")
        cache_connected = init_elasticsearch_cache()
        
        if cache_connected:
            print("✅ Elasticsearch conectado com sucesso")
            
            # Verificar status
            status = get_cache_status()
            print(f"📊 Índices encontrados: {status.get('indices_count', 0)}")
            print(f"📋 Total de documentos: {status.get('total_docs', 0):,}")
            print(f"💾 Espaço usado: {status.get('total_size_mb', 0):.1f} MB")
            
            # Exemplo de verificação de cache
            doc_ids = ['doc_0001', 'doc_0002', 'doc_0003']
            exists, existing, missing = check_embeddings_in_cache('embeddings_tfidf', doc_ids)
            
            print(f"🔍 Verificação de cache:")
            print(f"   Existem: {exists}")
            print(f"   Encontrados: {len(existing)}")
            print(f"   Faltando: {len(missing)}")
            
        else:
            print("⚠️  Elasticsearch não disponível")
            print("💡 Execute: docker-compose up -d")
            
    except ImportError:
        print("⚠️  Módulo elasticsearch_manager não encontrado")
        print("💡 Certifique-se de que está no diretório raiz do projeto")

def example_clustering():
    """Exemplo de clustering básico"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.datasets import fetch_20newsgroups
    
    # Carregar dados
    print("📥 Carregando dados para clustering...")
    newsgroups = fetch_20newsgroups(
        subset='train',
        categories=['sci.med', 'sci.crypt', 'rec.sport.baseball'],
        remove=('headers', 'footers', 'quotes')
    )
    
    # Limitar a 200 documentos
    texts = newsgroups.data[:200]
    true_labels = newsgroups.target[:200]
    
    # Gerar embeddings
    print("🔄 Gerando embeddings...")
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    embeddings = vectorizer.fit_transform(texts)
    
    # Clustering
    print("🔍 Aplicando clustering K-Means...")
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(embeddings.toarray())
    
    # Avaliação
    silhouette = silhouette_score(embeddings, cluster_labels)
    print(f"📊 Silhouette Score: {silhouette:.3f}")
    print(f"📊 Clusters encontrados: {len(set(cluster_labels))}")
    
    # Análise dos clusters
    print("📈 Análise dos clusters:")
    for i in range(3):
        cluster_mask = cluster_labels == i
        cluster_size = cluster_mask.sum()
        print(f"   Cluster {i}: {cluster_size} documentos")
        
        # Mostrar algumas palavras características
        cluster_embeddings = embeddings[cluster_mask]
        mean_embeddings = cluster_embeddings.mean(axis=0).A1
        top_words_idx = np.argsort(mean_embeddings)[-5:][::-1]
        feature_names = vectorizer.get_feature_names_out()
        
        top_words = [feature_names[idx] for idx in top_words_idx]
        print(f"      Palavras características: {', '.join(top_words)}")

if __name__ == "__main__":
    main()
