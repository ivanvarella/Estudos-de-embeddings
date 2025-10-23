#!/usr/bin/env python3
"""
Elasticsearch Helper Functions
===============================

Este módulo contém funções auxiliares para trabalhar com Elasticsearch,
especialmente para buscar grandes volumes de dados (>10.000 documentos).

Autor: Sistema de Embeddings e Clustering
Data: 2025-10
"""

import pandas as pd
from typing import Optional
from elasticsearch import Elasticsearch


def load_all_documents_from_elasticsearch(
    es_client: Elasticsearch,
    index_name: str = "documents_dataset",
    batch_size: int = 1000,
    scroll_timeout: str = '2m',
    verbose: bool = True
) -> pd.DataFrame:
    """
    Carrega TODOS os documentos do Elasticsearch usando Scroll API.
    
    🎓 CONCEITO EDUCACIONAL: SCROLL API DO ELASTICSEARCH
    ===================================================
    
    ### Por que precisamos da Scroll API?
    
    O Elasticsearch tem um limite padrão de **10.000 documentos** por busca simples
    (`index.max_result_window = 10000`). Isso é uma proteção de performance para
    evitar que buscas muito grandes consumam toda a memória do servidor.
    
    Quando tentamos buscar mais de 10.000 documentos com uma query normal:
    ```python
    # ❌ ISSO FALHA com 18.211 documentos!
    response = es.search(index="documents_dataset", size=20000)
    # BadRequestError: Result window is too large
    ```
    
    ### Como a Scroll API resolve isso?
    
    A Scroll API funciona como um "cursor" de banco de dados:
    
    1. **Snapshot (Foto dos dados)**:
       - Cria uma "foto" consistente dos dados no momento da busca
       - Os dados não mudam durante toda a busca
       - Garante que você não perca nem duplique documentos
    
    2. **Busca em Lotes**:
       - Busca 1000 documentos por vez (ou outro tamanho definido)
       - Retorna um "scroll_id" (cursor) para continuar de onde parou
       - Muito mais eficiente em memória
    
    3. **Iteração Eficiente**:
       - Usa o scroll_id para buscar o próximo lote
       - Continua até não haver mais dados
       - Elasticsearch mantém contexto no servidor
    
    4. **Limpeza de Recursos**:
       - Ao final, limpa o scroll_id
       - Libera recursos no servidor
    
    ### Alternativas e por que NÃO usá-las:
    
    ❌ **Múltiplas buscas com FROM/SIZE**:
    ```python
    # Busca 1: from=0, size=10000
    # Busca 2: from=10000, size=10000
    ```
    Problemas:
    - Muito ineficiente: cada busca reprocessa TODOS os docs anteriores
    - Consome muita memória no servidor
    - Pode ter limite total (from + size ≤ max_result_window)
    - Lenta para dados "profundos"
    
    ❌ **Aumentar max_result_window**:
    ```python
    PUT /index/_settings {"index.max_result_window": 50000}
    ```
    Problemas:
    - PERIGOSO: Pode crashar o Elasticsearch
    - Consome memória excessiva
    - Não é escalável
    - Vai contra boas práticas oficiais
    
    ✅ **Scroll API** (NOSSA ESCOLHA):
    - Recomendação oficial do Elasticsearch
    - Eficiente em memória e processamento
    - Consistente e confiável
    - Perfeita para "dump completo" de dados
    
    ### Fluxo de Execução:
    
    ```
    ┌─────────────────────────────────────────┐
    │ 1. INICIAR SCROLL                       │
    │    es.search(scroll='2m', size=1000)    │
    └──────────────┬──────────────────────────┘
                   │
                   ↓ Retorna: scroll_id + 1000 docs
    ┌─────────────────────────────────────────┐
    │ 2. CONTINUAR SCROLL (loop)              │
    │    es.scroll(scroll_id=scroll_id)       │
    └──────────────┬──────────────────────────┘
                   │
                   ↓ Retorna: novo scroll_id + próximos 1000 docs
                   │
                   ↓ Repete até não haver mais docs
    ┌─────────────────────────────────────────┐
    │ 3. LIMPAR SCROLL                        │
    │    es.clear_scroll(scroll_id=scroll_id) │
    └─────────────────────────────────────────┘
    ```
    
    ### Parâmetros:
    
    Args:
        es_client (Elasticsearch): 
            Cliente Elasticsearch já conectado.
            Exemplo: Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        index_name (str, optional): 
            Nome do índice a buscar. 
            Padrão: "documents_dataset"
        
        batch_size (int, optional): 
            Número de documentos por lote.
            - Menor (500): Mais requisições, menos memória por vez
            - Maior (5000): Menos requisições, mais memória por vez
            - Recomendado: 1000 (bom equilíbrio)
            Padrão: 1000
        
        scroll_timeout (str, optional): 
            Tempo que o Elasticsearch mantém o contexto de scroll ativo.
            - '1m': 1 minuto (busca rápida)
            - '2m': 2 minutos (recomendado)
            - '5m': 5 minutos (busca lenta ou debug)
            Após esse tempo, o scroll expira automaticamente.
            Padrão: '2m'
        
        verbose (bool, optional):
            Se True, mostra progresso detalhado.
            Se False, execução silenciosa.
            Padrão: True
    
    Returns:
        pd.DataFrame: 
            DataFrame com todos os documentos do índice, contendo colunas:
            - doc_id: ID único do documento (ex: "doc_0000")
            - text: Texto completo do documento
            - category: Categoria/classe do documento
            - target: Código numérico da categoria
            
            O DataFrame é ordenado por doc_id para garantir consistência.
    
    Raises:
        Exception: 
            Qualquer erro durante a busca (conexão, índice não existe, etc.)
            O scroll_id é automaticamente limpo mesmo em caso de erro.
    
    Example:
        >>> from elasticsearch import Elasticsearch
        >>> es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        >>> df = load_all_documents_from_elasticsearch(es)
        📊 Total de documentos disponíveis: 18,211
        🔄 Iniciando busca em lotes...
           Lote 1: 1,000 docs | Total acumulado: 1,000/18,211
           Lote 2: 1,000 docs | Total acumulado: 2,000/18,211
           ...
        ✅ Scroll concluído e recursos liberados
        >>> print(df.shape)
        (18211, 4)
    
    Notes:
        - A Scroll API cria um snapshot dos dados no momento da busca inicial
        - Mudanças no índice durante a busca NÃO serão refletidas nos resultados
        - O scroll_id é automaticamente limpo ao final ou em caso de erro
        - Esta função é thread-safe (cada chamada tem seu próprio scroll_id)
    
    See Also:
        - Documentação oficial: https://www.elastic.co/guide/en/elasticsearch/reference/current/scroll-api.html
        - Search After API: Alternativa moderna para paginação em tempo real
    """
    
    if verbose:
        print(f"🔄 Buscando documentos do índice '{index_name}'")
        print(f"   Método: Scroll API (recomendado para >10k docs)")
        print(f"   Tamanho do lote: {batch_size:,} documentos")
        print(f"   Timeout do scroll: {scroll_timeout}")
    
    all_documents = []
    scroll_id = None
    
    try:
        # =================================================================
        # PASSO 1: INICIAR SCROLL
        # =================================================================
        # Primeira busca que cria o "snapshot" e retorna o scroll_id
        
        response = es_client.search(
            index=index_name,
            scroll=scroll_timeout,  # Manter contexto ativo
            size=batch_size,        # Docs por lote
            body={
                "query": {"match_all": {}},  # Buscar todos os docs
                "_source": ["doc_id", "text", "category", "target"]  # Campos desejados
            }
        )
        
        # Extrair informações da resposta
        scroll_id = response['_scroll_id']  # Cursor para próximas buscas
        hits = response['hits']['hits']      # Documentos encontrados
        total_docs = response['hits']['total']['value']  # Total disponível
        
        if verbose:
            print(f"\n📊 Total de documentos disponíveis: {total_docs:,}")
            print(f"🔄 Iniciando busca em lotes...")
        
        # Adicionar primeiro lote
        all_documents.extend(hits)
        
        if verbose:
            print(f"   Lote 1: {len(hits):,} docs | Total acumulado: {len(all_documents):,}/{total_docs:,}")
        
        # =================================================================
        # PASSO 2: CONTINUAR SCROLL
        # =================================================================
        # Buscar próximos lotes até não haver mais dados
        
        batch_number = 2
        
        while len(hits) > 0:  # Enquanto houver documentos
            # Buscar próximo lote usando scroll_id
            response = es_client.scroll(
                scroll_id=scroll_id,
                scroll=scroll_timeout  # Renovar timeout
            )
            
            # Atualizar scroll_id e hits
            scroll_id = response['_scroll_id']
            hits = response['hits']['hits']
            
            # Se houver documentos, adicionar à lista
            if len(hits) > 0:
                all_documents.extend(hits)
                
                if verbose:
                    print(f"   Lote {batch_number}: {len(hits):,} docs | Total acumulado: {len(all_documents):,}/{total_docs:,}")
                
                batch_number += 1
        
        # =================================================================
        # PASSO 3: LIMPAR SCROLL
        # =================================================================
        # Liberar recursos no servidor Elasticsearch
        
        try:
            es_client.clear_scroll(scroll_id=scroll_id)
            if verbose:
                print(f"\n✅ Scroll concluído e recursos liberados")
        except Exception:
            # Scroll pode ter expirado automaticamente
            if verbose:
                print(f"\n⚠️  Scroll expirou automaticamente (normal)")
        
        # =================================================================
        # PASSO 4: CONVERTER PARA DATAFRAME
        # =================================================================
        # Processar documentos para formato pandas
        
        if verbose:
            print(f"\n📊 Processando {len(all_documents):,} documentos em DataFrame...")
        
        documents_data = []
        
        for hit in all_documents:
            source = hit['_source']
            documents_data.append({
                'doc_id': source['doc_id'],
                'text': source['text'],
                'category': source['category'],
                'target': source['target']
            })
        
        df = pd.DataFrame(documents_data)
        
        # Ordenar por doc_id para garantir ordem consistente entre notebooks
        df = df.sort_values('doc_id').reset_index(drop=True)
        
        if verbose:
            print(f"✅ DataFrame criado com sucesso!")
        
        return df
        
    except Exception as e:
        if verbose:
            print(f"\n❌ ERRO ao carregar documentos: {e}")
        
        # Tentar limpar scroll mesmo em caso de erro
        if scroll_id:
            try:
                es_client.clear_scroll(scroll_id=scroll_id)
                if verbose:
                    print("   (Scroll limpo após erro)")
            except:
                pass
        
        # Re-raise o erro original
        raise


def print_dataframe_summary(df: pd.DataFrame, expected_docs: Optional[int] = None):
    """
    Imprime um resumo detalhado do DataFrame carregado.
    
    Args:
        df: DataFrame com os documentos
        expected_docs: Número esperado de documentos (opcional)
    """
    print(f"\n{'='*60}")
    print(f"✅ DATASET CARREGADO COM SUCESSO!")
    print(f"{'='*60}")
    print(f"📊 Shape: {df.shape}")
    print(f"📋 Colunas: {list(df.columns)}")
    print(f"🏷️  Classes únicas: {df['category'].nunique()}")
    print(f"🔢 Total de documentos: {len(df):,}")
    
    # Mostrar amostra de IDs
    doc_ids = df['doc_id'].tolist()
    print(f"🔑 IDs (amostra): {doc_ids[:3]} ... {doc_ids[-3:]}")
    
    # Validação se fornecido expected_docs
    if expected_docs:
        tolerance = 1000
        print(f"\n🔍 VALIDAÇÃO:")
        if abs(len(df) - expected_docs) <= tolerance:
            print(f"   ✅ PASSOU: {len(df):,} documentos")
            print(f"   ✅ Dentro da expectativa: ~{expected_docs:,} ±{tolerance:,}")
        else:
            print(f"   ⚠️  AVISO: {len(df):,} documentos encontrados")
            print(f"   ⚠️  Esperado: ~{expected_docs:,} ±{tolerance:,}")
            print(f"   💡 Verifique se o Notebook 1 foi executado completamente")

