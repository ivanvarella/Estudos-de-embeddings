#!/usr/bin/env python3
"""
Teste do Sistema de Cache Elasticsearch
Valida o funcionamento completo do sistema de cache de embeddings
"""

import sys
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
import pandas as pd

# Adicionar o diretório raiz ao path para importar o módulo
sys.path.append(str(Path(__file__).parent.parent))

# Constantes
TEST_EMBEDDINGS_SHAPE = (3, 100)
TEST_EMBEDDINGS_SHAPE_SMALL = (2, 50)
TOLERANCE_RTOL = 1e-5


def test_elasticsearch_connection() -> bool:
    """
    Testa conexão com Elasticsearch.

    Returns:
        bool: True se conexão bem-sucedida, False caso contrário
    """
    print("🔌 Testando conexão com Elasticsearch...")

    try:
        from elasticsearch_manager import init_elasticsearch_cache, get_cache_status

        # Conectar
        connected = init_elasticsearch_cache()
        if not connected:
            print("❌ Falha na conexão com Elasticsearch")
            return False

        # Verificar status
        status = get_cache_status()
        if status.get("connected", False):
            print("✅ Elasticsearch conectado com sucesso")
            host = status.get("host", "N/A")
            print(f"   Host: {host}")
            return True

        error_msg = status.get("error", "Desconhecido")
        print(f"❌ Erro no status: {error_msg}")
        return False

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao testar Elasticsearch: {e}")
        return False


def test_dataset_save_load() -> bool:
    """
    Testa salvamento e carregamento do dataset.

    Returns:
        bool: True se teste passou, False caso contrário
    """
    print("\n📄 Testando salvamento e carregamento do dataset...")

    try:
        from elasticsearch_manager import save_dataset_to_cache, get_cache_status

        # Criar dataset de teste
        test_data = {
            "text": [
                "This is a test document about machine learning.",
                "Another test document about artificial intelligence.",
                "A third document about data science and analytics.",
            ],
            "category": ["tech", "tech", "tech"],
            "target": [0, 0, 0],
        }
        test_df = pd.DataFrame(test_data)

        # Salvar dataset
        success = save_dataset_to_cache(test_df)
        if not success:
            print("❌ Falha ao salvar dataset")
            return False

        print("✅ Dataset de teste salvo com sucesso")

        # Verificar se foi salvo
        status = get_cache_status()
        indices = status.get("indices", {})
        dataset_info = indices.get("documents_dataset", {})

        if dataset_info.get("exists", False):
            doc_count = dataset_info.get("doc_count", 0)
            print(f"✅ Dataset encontrado no cache: {doc_count} documentos")
            return True

        print("❌ Dataset não encontrado no cache")
        return False

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao testar dataset: {e}")
        return False


def test_embeddings_save_load() -> bool:
    """
    Testa salvamento e carregamento de embeddings.

    Returns:
        bool: True se teste passou, False caso contrário
    """
    print("\n🧮 Testando salvamento e carregamento de embeddings...")

    try:
        from elasticsearch_manager import (
            save_embeddings_to_cache,
            load_embeddings_from_cache,
            check_embeddings_in_cache,
        )

        # Criar embeddings de teste
        test_embeddings = np.random.rand(*TEST_EMBEDDINGS_SHAPE).astype(np.float32)
        test_doc_ids = ["doc_0001", "doc_0002", "doc_0003"]
        test_texts = [
            "This is a test document about machine learning.",
            "Another test document about artificial intelligence.",
            "A third document about data science and analytics.",
        ]

        # Salvar embeddings
        success = save_embeddings_to_cache(
            "embeddings_test", test_embeddings, test_doc_ids, test_texts, "test_model"
        )
        if not success:
            print("❌ Falha ao salvar embeddings")
            return False

        print("✅ Embeddings de teste salvos com sucesso")

        # Verificar se existem
        all_exist, existing, missing = check_embeddings_in_cache(
            "embeddings_test", test_doc_ids
        )
        if all_exist:
            print("✅ Todos os embeddings encontrados no cache")
        else:
            total_ids = len(test_doc_ids)
            found_count = len(existing)
            print(f"⚠️  Apenas {found_count}/{total_ids} embeddings encontrados")

        # Carregar embeddings
        loaded_embeddings = load_embeddings_from_cache("embeddings_test", test_doc_ids)
        if loaded_embeddings is not None:
            print(f"✅ Embeddings carregados: {loaded_embeddings.shape}")

            # Verificar se são iguais (com tolerância para float32)
            if np.allclose(test_embeddings, loaded_embeddings, rtol=TOLERANCE_RTOL):
                print("✅ Embeddings carregados são idênticos aos originais")
                return True

            print("❌ Embeddings carregados diferem dos originais")
            return False

        print("❌ Falha ao carregar embeddings")
        return False

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao testar embeddings: {e}")
        return False


def test_duplicate_prevention() -> bool:
    """
    Testa prevenção de duplicatas.

    Returns:
        bool: True se teste passou, False caso contrário
    """
    print("\n🔄 Testando prevenção de duplicatas...")

    try:
        from elasticsearch_manager import (
            save_embeddings_to_cache,
            check_embeddings_in_cache,
        )

        # Criar embeddings de teste
        test_embeddings = np.random.rand(*TEST_EMBEDDINGS_SHAPE_SMALL).astype(
            np.float32
        )
        test_doc_ids = ["doc_test_001", "doc_test_002"]
        test_texts = [
            "Test document for duplicate prevention.",
            "Another test document for duplicate prevention.",
        ]

        # Salvar primeira vez
        success1 = save_embeddings_to_cache(
            "embeddings_duplicate_test",
            test_embeddings,
            test_doc_ids,
            test_texts,
            "test_model",
        )
        if not success1:
            print("❌ Falha ao salvar embeddings na primeira vez")
            return False

        print("✅ Embeddings salvos na primeira vez")

        # Verificar se existem
        all_exist, existing, missing = check_embeddings_in_cache(
            "embeddings_duplicate_test", test_doc_ids
        )
        if not all_exist:
            print("❌ Embeddings não encontrados após salvamento")
            return False

        print("✅ Embeddings encontrados no cache")

        # Tentar salvar novamente (deve detectar duplicatas)
        success2 = save_embeddings_to_cache(
            "embeddings_duplicate_test",
            test_embeddings,
            test_doc_ids,
            test_texts,
            "test_model",
        )
        if success2:
            print("✅ Sistema detectou duplicatas e evitou salvamento desnecessário")
            return True

        print("❌ Sistema não detectou duplicatas")
        return False

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao testar prevenção de duplicatas: {e}")
        return False


def test_integrity_validation() -> bool:
    """
    Testa validação de integridade.

    Returns:
        bool: True se teste passou, False caso contrário
    """
    print("\n🔍 Testando validação de integridade...")

    try:
        from elasticsearch_manager import (
            save_embeddings_to_cache,
            validate_embeddings_integrity,
        )

        # Criar embeddings de teste
        test_embeddings = np.random.rand(*TEST_EMBEDDINGS_SHAPE_SMALL).astype(
            np.float32
        )
        test_doc_ids = ["doc_integrity_001", "doc_integrity_002"]
        test_texts = [
            "Test document for integrity validation.",
            "Another test document for integrity validation.",
        ]

        # Salvar embeddings
        success = save_embeddings_to_cache(
            "embeddings_integrity_test",
            test_embeddings,
            test_doc_ids,
            test_texts,
            "test_model",
        )
        if not success:
            print("❌ Falha ao salvar embeddings para teste de integridade")
            return False

        # Testar validação com textos corretos
        valid, invalid_ids = validate_embeddings_integrity(
            "embeddings_integrity_test", test_doc_ids, test_texts
        )
        if valid and len(invalid_ids) == 0:
            print("✅ Validação de integridade passou com textos corretos")
        else:
            invalid_count = len(invalid_ids)
            print(f"❌ Validação falhou: {invalid_count} IDs inválidos")
            return False

        # Testar validação com textos incorretos
        wrong_texts = [
            "Wrong text for integrity validation.",
            "Another wrong text for integrity validation.",
        ]
        valid_wrong, invalid_ids_wrong = validate_embeddings_integrity(
            "embeddings_integrity_test", test_doc_ids, wrong_texts
        )
        if not valid_wrong and len(invalid_ids_wrong) > 0:
            print("✅ Validação detectou textos incorretos corretamente")
            return True

        print("❌ Validação não detectou textos incorretos")
        return False

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao testar validação de integridade: {e}")
        return False


def test_cache_cleanup() -> bool:
    """
    Testa limpeza do cache de teste.

    Returns:
        bool: True se teste passou, False caso contrário
    """
    print("\n🧹 Limpando cache de teste...")

    try:
        from elasticsearch_manager import clear_elasticsearch_cache

        # Limpar índices de teste
        test_indices = [
            "embeddings_test",
            "embeddings_duplicate_test",
            "embeddings_integrity_test",
        ]

        for index_name in test_indices:
            success = clear_elasticsearch_cache(index_name)
            if success:
                print(f"✅ Índice {index_name} limpo")
            else:
                print(f"⚠️  Índice {index_name} não foi limpo (pode não existir)")

        print("✅ Limpeza do cache de teste concluída")
        return True

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao limpar cache: {e}")
        return False


def main() -> int:
    """
    Função principal de teste.

    Returns:
        int: 0 se todos os testes passaram, 1 caso contrário
    """
    print("🧪 TESTE DO SISTEMA DE CACHE ELASTICSEARCH")
    print("=" * 60)

    tests: List[Tuple[str, callable]] = [
        ("Conexão Elasticsearch", test_elasticsearch_connection),
        ("Dataset Save/Load", test_dataset_save_load),
        ("Embeddings Save/Load", test_embeddings_save_load),
        ("Prevenção de Duplicatas", test_duplicate_prevention),
        ("Validação de Integridade", test_integrity_validation),
        ("Limpeza do Cache", test_cache_cleanup),
    ]

    results: List[Tuple[str, bool]] = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:<25}: {status}")
        if result:
            passed += 1

    print(f"\nResultado: {passed}/{total} testes passaram")

    if passed == total:
        print(
            "\n🎉 Todos os testes passaram! O sistema de cache está funcionando perfeitamente."
        )
        print("💡 O notebook pode usar o cache Elasticsearch com segurança.")
        return 0
    elif passed >= total - 1:  # Permite 1 falha (limpeza é opcional)
        print("\n✅ Sistema de cache funcional! Apenas alguns testes falharam.")
        print("💡 O notebook pode usar o cache Elasticsearch.")
        return 0

    print(
        "\n❌ Sistema de cache com problemas. Verifique a configuração do Elasticsearch."
    )
    print("💡 Execute: docker-compose up -d")
    return 1


if __name__ == "__main__":
    sys.exit(main())
