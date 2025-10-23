#!/usr/bin/env python3
"""
Elasticsearch Manager para Cache de Embeddings
Sistema inteligente de cache com verificação de duplicatas e validação de integridade
"""

import os
import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, ConnectionError
import warnings


class ElasticsearchEmbeddingsCache:
    """
    Gerenciador de cache de embeddings no Elasticsearch com verificação inteligente
    """

    def __init__(self, host="localhost", port=9200, timeout=30, max_retries=3):
        """
        Inicializa o gerenciador de cache

        Args:
            host: Host do Elasticsearch
            port: Porta do Elasticsearch
            timeout: Timeout para operações (segundos)
            max_retries: Número máximo de tentativas
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.max_retries = max_retries
        self.es = None
        self.connected = False

        # Configurações dos índices
        self.indices_config = {
            "documents_dataset": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "text": {"type": "text", "analyzer": "standard"},
                            "category": {"type": "keyword"},
                            "target": {"type": "integer"},
                            "text_hash": {"type": "keyword"},
                            "created_at": {"type": "date"},
                        }
                    }
                }
            },
            "embeddings_tfidf": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 4096},  # TF-IDF com max_features=4096 (limite máximo do Elasticsearch)
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
            "embeddings_word2vec": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 100},
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
            "embeddings_bert": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 768},
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
            "embeddings_sbert": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 384},
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
            "embeddings_openai": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 1536},
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
            # Índices de teste
            "embeddings_test": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 100},
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
            "embeddings_duplicate_test": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 50},
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
            "embeddings_integrity_test": {
                "mapping": {
                    "mappings": {
                        "properties": {
                            "doc_id": {"type": "keyword"},
                            "embedding": {"type": "dense_vector", "dims": 50},
                            "metadata": {
                                "properties": {
                                    "model_type": {"type": "keyword"},
                                    "model_version": {"type": "keyword"},
                                    "generated_at": {"type": "date"},
                                    "dimensions": {"type": "integer"},
                                    "text_hash": {"type": "keyword"},
                                }
                            },
                        }
                    }
                }
            },
        }

    def connect(self) -> bool:
        """
        Conecta ao Elasticsearch

        Returns:
            bool: True se conectou com sucesso
        """
        try:
            self.es = Elasticsearch(
                [{"host": self.host, "port": self.port, "scheme": "http"}],
                request_timeout=self.timeout,
                max_retries=self.max_retries,
                retry_on_timeout=True,
            )

            # Testar conexão
            if self.es.ping():
                self.connected = True
                print(f"✅ Conectado ao Elasticsearch ({self.host}:{self.port})")
                return True
            else:
                print(
                    f"❌ Falha na conexão com Elasticsearch ({self.host}:{self.port})"
                )
                return False

        except Exception as e:
            print(f"❌ Erro ao conectar com Elasticsearch: {e}")
            self.connected = False
            return False

    def _generate_doc_id(self, index: int) -> str:
        """Gera ID único para documento"""
        return f"doc_{index:04d}"

    def _generate_text_hash(self, text: str) -> str:
        """Gera hash MD5 do texto para validação"""
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def _check_index_exists(self, index_name: str) -> bool:
        """Verifica se índice existe"""
        try:
            return self.es.indices.exists(index=index_name)
        except:
            return False

    def _check_dimensions_compatibility(
        self, index_name: str, expected_dims: int
    ) -> bool:
        """Verifica se as dimensões do índice são compatíveis com os embeddings"""
        try:
            # Obter mapeamento do índice
            mapping = self.es.indices.get_mapping(index=index_name)

            # Extrair dimensões do campo embedding
            if index_name in mapping:
                properties = (
                    mapping[index_name].get("mappings", {}).get("properties", {})
                )
                embedding_config = properties.get("embedding", {})
                stored_dims = embedding_config.get("dims", 0)

                # Verificar compatibilidade
                if stored_dims != expected_dims:
                    print(
                        f"   Dimensões incompatíveis: esperado {expected_dims}, encontrado {stored_dims}"
                    )
                    return False
                return True
            return True
        except Exception as e:
            print(f"   Erro ao verificar dimensões: {e}")
            return True  # Se não conseguir verificar, assume compatível

    def create_index(self, index_name: str) -> bool:
        """
        Cria índice se não existir

        Args:
            index_name: Nome do índice

        Returns:
            bool: True se criado com sucesso
        """
        if not self.connected:
            print("❌ Não conectado ao Elasticsearch")
            return False

        if index_name not in self.indices_config:
            print(f"❌ Índice '{index_name}' não configurado")
            return False

        try:
            if self._check_index_exists(index_name):
                print(f"✅ Índice '{index_name}' já existe")
                return True

            mapping = self.indices_config[index_name]["mapping"]
            self.es.indices.create(index=index_name, body=mapping)
            print(f"✅ Índice '{index_name}' criado com sucesso")
            return True

        except Exception as e:
            print(f"❌ Erro ao criar índice '{index_name}': {e}")
            return False

    def save_dataset(self, df: pd.DataFrame) -> bool:
        """
        Salva dataset completo no Elasticsearch com IDs únicos e proteção robusta contra duplicatas

        Args:
            df: DataFrame com colunas 'text', 'category', 'target'

        Returns:
            bool: True se salvo com sucesso ou já existe
        """
        if not self.connected:
            print("❌ Não conectado ao Elasticsearch")
            return False

        index_name = "documents_dataset"

        # Verificar configuração de força de regeneração
        import os

        force_regenerate = (
            os.getenv("FORCE_REGENERATE_EMBEDDINGS", "false").lower() == "true"
        )

        # Verificar se índice já existe
        if self._check_index_exists(index_name):
            try:
                # Obter contagem de documentos
                count_response = self.es.count(index=index_name)
                doc_count = count_response["count"]
                expected_count = len(df)

                print(
                    f"📊 Índice '{index_name}' já existe com {doc_count:,} documentos"
                )

                # Se número de documentos está correto
                if doc_count == expected_count:
                    # Validar integridade dos dados (amostra)
                    print("🔍 Verificando integridade dos dados...")
                    sample_size = min(100, expected_count)
                    sample_indices = list(
                        range(0, expected_count, max(1, expected_count // sample_size))
                    )[:sample_size]

                    integrity_ok = True
                    for idx in sample_indices:
                        doc_id = self._generate_doc_id(idx)
                        try:
                            response = self.es.get(index=index_name, id=doc_id)
                            stored_hash = response["_source"].get("text_hash", "")
                            expected_hash = self._generate_text_hash(
                                df.iloc[idx]["text"]
                            )
                            if stored_hash != expected_hash:
                                integrity_ok = False
                                print(
                                    f"   ⚠️  Integridade comprometida no documento {doc_id}"
                                )
                                break
                        except:
                            integrity_ok = False
                            break

                    if integrity_ok and not force_regenerate:
                        print(
                            f"✅ Dados já existem e estão íntegros - PULANDO salvamento"
                        )
                        print(
                            f"💡 Use FORCE_REGENERATE_EMBEDDINGS=true para forçar re-salvamento"
                        )
                        return True
                    elif not integrity_ok:
                        print(f"⚠️  Dados corrompidos detectados - RE-SALVANDO")
                    elif force_regenerate:
                        print(f"🔄 FORCE_REGENERATE ativo - RE-SALVANDO")

                    # Deletar índice para re-salvar
                    print(f"🗑️  Deletando índice existente...")
                    self.es.indices.delete(index=index_name)

                elif doc_count != expected_count:
                    print(
                        f"⚠️  Contagem incorreta (esperado: {expected_count:,}, encontrado: {doc_count:,})"
                    )
                    print(f"🗑️  Deletando índice para re-salvar...")
                    self.es.indices.delete(index=index_name)

            except Exception as e:
                print(f"⚠️  Erro ao verificar índice: {e}")
                print(f"🔄 Tentando re-salvar...")

        # Criar índice
        if not self.create_index(index_name):
            return False

        try:
            # Preparar documentos para bulk insert
            bulk_data = []
            current_time = datetime.now().isoformat()

            for idx, row in df.iterrows():
                doc_id = self._generate_doc_id(idx)
                text_hash = self._generate_text_hash(row["text"])

                doc = {
                    "doc_id": doc_id,
                    "text": row["text"],
                    "category": row["category"],
                    "target": int(row["target"]),
                    "text_hash": text_hash,
                    "created_at": current_time,
                }

                bulk_data.append({"_index": index_name, "_id": doc_id, "_source": doc})

            # Bulk insert
            from elasticsearch.helpers import bulk

            success_count, failed_items = bulk(self.es, bulk_data, chunk_size=1000)

            print(f"✅ Dataset salvo: {success_count:,} documentos em '{index_name}'")
            if failed_items:
                print(f"⚠️  {len(failed_items)} documentos falharam")

            return success_count > 0

        except Exception as e:
            print(f"❌ Erro ao salvar dataset: {e}")
            return False

    def check_embeddings_exist(
        self, index_name: str, doc_ids: List[str]
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Verifica quais embeddings existem e quais estão faltando usando Scroll API

        Args:
            index_name: Nome do índice de embeddings
            doc_ids: Lista de IDs de documentos

        Returns:
            Tuple[bool, List[str], List[str]]: (todos_existem, ids_existentes, ids_faltando)
        """
        if not self.connected:
            return False, [], doc_ids

        try:
            # Verificar se índice existe
            if not self._check_index_exists(index_name):
                return False, [], doc_ids

            # Buscar documentos existentes usando Scroll API (para >10k docs)
            existing_ids = []
            scroll_id = None
            
            try:
                # Iniciar scroll
                response = self.es.search(
                    index=index_name,
                    scroll='2m',
                    size=1000,
                    body={
                        "query": {"terms": {"doc_id": doc_ids}},
                        "_source": ["doc_id"]
                    }
                )
                
                scroll_id = response['_scroll_id']
                hits = response['hits']['hits']
                existing_ids.extend([hit["_source"]["doc_id"] for hit in hits])
                
                # Continuar scroll
                while len(hits) > 0:
                    response = self.es.scroll(scroll_id=scroll_id, scroll='2m')
                    scroll_id = response['_scroll_id']
                    hits = response['hits']['hits']
                    if len(hits) > 0:
                        existing_ids.extend([hit["_source"]["doc_id"] for hit in hits])
                
                # Limpar scroll
                try:
                    self.es.clear_scroll(scroll_id=scroll_id)
                except:
                    pass
                    
            except Exception as scroll_error:
                # Limpar scroll em caso de erro
                if scroll_id:
                    try:
                        self.es.clear_scroll(scroll_id=scroll_id)
                    except:
                        pass
                raise scroll_error
            
            # Identificar IDs faltando
            existing_ids_set = set(existing_ids)
            missing_ids = [doc_id for doc_id in doc_ids if doc_id not in existing_ids_set]
            
            all_exist = len(missing_ids) == 0

            return all_exist, existing_ids, missing_ids

        except Exception as e:
            print(f"❌ Erro ao verificar embeddings: {e}")
            return False, [], doc_ids

    def validate_embeddings_integrity(
        self, index_name: str, doc_ids: List[str], expected_texts: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Valida integridade dos embeddings comparando hashes dos textos usando Scroll API

        Args:
            index_name: Nome do índice de embeddings
            doc_ids: Lista de IDs de documentos
            expected_texts: Lista de textos originais

        Returns:
            Tuple[bool, List[str]]: (todos_validos, ids_invalidos)
        """
        if not self.connected:
            return False, doc_ids

        try:
            # Buscar embeddings com metadata usando Scroll API (para >10k docs)
            doc_id_to_hash = {}
            scroll_id = None
            
            try:
                # Iniciar scroll
                response = self.es.search(
                    index=index_name,
                    scroll='2m',
                    size=1000,
                    body={
                        "query": {"terms": {"doc_id": doc_ids}},
                        "_source": ["doc_id", "metadata.text_hash"]
                    }
                )
                
                scroll_id = response['_scroll_id']
                hits = response['hits']['hits']
                
                for hit in hits:
                    doc_id_to_hash[hit["_source"]["doc_id"]] = hit["_source"]["metadata"]["text_hash"]
                
                # Continuar scroll
                while len(hits) > 0:
                    response = self.es.scroll(scroll_id=scroll_id, scroll='2m')
                    scroll_id = response['_scroll_id']
                    hits = response['hits']['hits']
                    
                    if len(hits) > 0:
                        for hit in hits:
                            doc_id_to_hash[hit["_source"]["doc_id"]] = hit["_source"]["metadata"]["text_hash"]
                
                # Limpar scroll
                try:
                    self.es.clear_scroll(scroll_id=scroll_id)
                except:
                    pass
                    
            except Exception as scroll_error:
                # Limpar scroll em caso de erro
                if scroll_id:
                    try:
                        self.es.clear_scroll(scroll_id=scroll_id)
                    except:
                        pass
                raise scroll_error

            # Validar cada documento
            invalid_ids = []
            for i, doc_id in enumerate(doc_ids):
                if doc_id in doc_id_to_hash:
                    expected_hash = self._generate_text_hash(expected_texts[i])
                    stored_hash = doc_id_to_hash[doc_id]

                    if expected_hash != stored_hash:
                        invalid_ids.append(doc_id)
                else:
                    invalid_ids.append(doc_id)

            all_valid = len(invalid_ids) == 0
            return all_valid, invalid_ids

        except Exception as e:
            print(f"❌ Erro ao validar integridade: {e}")
            return False, doc_ids

    def save_embeddings(
        self,
        index_name: str,
        embeddings: np.ndarray,
        doc_ids: List[str],
        texts: List[str],
        model_type: str,
        model_version: str = "1.0",
    ) -> bool:
        """
        Salva embeddings no Elasticsearch com verificação de duplicatas

        Args:
            index_name: Nome do índice
            embeddings: Array de embeddings (n_docs, n_dims)
            doc_ids: Lista de IDs dos documentos
            texts: Lista de textos originais
            model_type: Tipo do modelo (tfidf, word2vec, bert, etc.)
            model_version: Versão do modelo

        Returns:
            bool: True se salvo com sucesso
        """
        if not self.connected:
            print("❌ Não conectado ao Elasticsearch")
            return False

        # Verificar se índice existe
        if not self.create_index(index_name):
            return False

        try:
            # Verificar quais embeddings já existem
            all_exist, existing_ids, missing_ids = self.check_embeddings_exist(
                index_name, doc_ids
            )

            if all_exist:
                print(f"✅ Todos os embeddings já existem em '{index_name}'")
                return True

            # Validar integridade dos existentes
            if existing_ids:
                valid, invalid_ids = self.validate_embeddings_integrity(
                    index_name,
                    existing_ids,
                    [texts[doc_ids.index(doc_id)] for doc_id in existing_ids],
                )

                if not valid:
                    print(
                        f"⚠️  {len(invalid_ids)} embeddings inválidos encontrados, serão regenerados"
                    )
                    missing_ids.extend(invalid_ids)

            if not missing_ids:
                print(f"✅ Todos os embeddings válidos já existem em '{index_name}'")
                return True

            # Preparar documentos para bulk insert
            bulk_data = []
            current_time = datetime.now().isoformat()

            for doc_id in missing_ids:
                idx = doc_ids.index(doc_id)
                text_hash = self._generate_text_hash(texts[idx])

                # Normalizar vetor para evitar vetores zero
                embedding_vector = embeddings[idx].copy()
                if np.linalg.norm(embedding_vector) == 0:
                    # Se vetor é zero, usar vetor pequeno aleatório
                    embedding_vector = np.random.normal(0, 0.01, embedding_vector.shape)

                doc = {
                    "doc_id": doc_id,
                    "embedding": embedding_vector.tolist(),
                    "metadata": {
                        "model_type": model_type,
                        "model_version": model_version,
                        "generated_at": current_time,
                        "dimensions": embeddings.shape[1],
                        "text_hash": text_hash,
                    },
                }

                bulk_data.append({"_index": index_name, "_id": doc_id, "_source": doc})

            # Bulk insert apenas dos faltantes
            from elasticsearch.helpers import bulk

            success_count, failed_items = bulk(
                self.es, bulk_data, chunk_size=1000, raise_on_error=False
            )

            print(
                f"✅ Embeddings salvos: {success_count} novos documentos em '{index_name}'"
            )

            # Aguardar indexação (Elasticsearch precisa de tempo para indexar)
            if success_count > 0:
                import time

                time.sleep(1)  # 1 segundo para garantir que os dados sejam indexados
            if failed_items:
                print(f"⚠️  {len(failed_items)} documentos falharam")
                for item in failed_items:
                    print(f"   Erro: {item}")
                return False

            return success_count > 0

        except Exception as e:
            print(f"❌ Erro ao salvar embeddings: {e}")
            return False

    def load_embeddings(
        self, index_name: str, doc_ids: List[str]
    ) -> Optional[np.ndarray]:
        """
        Carrega embeddings do Elasticsearch usando Scroll API

        Args:
            index_name: Nome do índice
            doc_ids: Lista de IDs dos documentos

        Returns:
            np.ndarray: Array de embeddings ou None se erro
        """
        if not self.connected:
            print("❌ Não conectado ao Elasticsearch")
            return None

        try:
            # Buscar embeddings usando Scroll API para suportar >10k docs
            embeddings_dict = {}
            scroll_id = None
            
            try:
                # Iniciar scroll
                response = self.es.search(
                    index=index_name,
                    scroll='2m',
                    size=1000,
                    body={
                        "query": {"terms": {"doc_id": doc_ids}},
                        "_source": ["doc_id", "embedding"]
                    }
                )
                
                scroll_id = response['_scroll_id']
                hits = response['hits']['hits']
                
                # Processar primeiro lote
                for hit in hits:
                    embeddings_dict[hit["_source"]["doc_id"]] = hit["_source"]["embedding"]
                
                # Continuar scroll para buscar mais lotes
                while len(hits) > 0:
                    response = self.es.scroll(scroll_id=scroll_id, scroll='2m')
                    scroll_id = response['_scroll_id']
                    hits = response['hits']['hits']
                    
                    if len(hits) > 0:
                        for hit in hits:
                            embeddings_dict[hit["_source"]["doc_id"]] = hit["_source"]["embedding"]
                
                # Limpar scroll
                try:
                    self.es.clear_scroll(scroll_id=scroll_id)
                except:
                    pass
                    
            except Exception as scroll_error:
                # Limpar scroll em caso de erro
                if scroll_id:
                    try:
                        self.es.clear_scroll(scroll_id=scroll_id)
                    except:
                        pass
                raise scroll_error

            if len(embeddings_dict) == 0:
                print(f"❌ Nenhum embedding encontrado em '{index_name}'")
                return None

            # Organizar embeddings na ordem correta dos doc_ids
            embeddings = []
            for doc_id in doc_ids:
                if doc_id in embeddings_dict:
                    embeddings.append(embeddings_dict[doc_id])
                else:
                    print(f"⚠️  Embedding não encontrado para {doc_id}")
                    return None

            embeddings_array = np.array(embeddings)
            print(
                f"✅ Embeddings carregados: {embeddings_array.shape} de '{index_name}'"
            )
            return embeddings_array

        except Exception as e:
            print(f"❌ Erro ao carregar embeddings: {e}")
            return None

    def get_cache_status(self) -> Dict[str, Any]:
        """
        Retorna status completo do cache

        Returns:
            Dict com informações do cache
        """
        if not self.connected:
            return {"connected": False, "error": "Não conectado ao Elasticsearch"}

        try:
            status = {
                "connected": True,
                "host": f"{self.host}:{self.port}",
                "indices": {},
                "total_docs": 0,
                "total_size_mb": 0,
            }

            # Verificar cada índice
            for index_name in self.indices_config.keys():
                if self._check_index_exists(index_name):
                    # Contar documentos
                    count_response = self.es.count(index=index_name)
                    doc_count = count_response["count"]

                    # Obter estatísticas de tamanho
                    stats_response = self.es.indices.stats(index=index_name)
                    size_bytes = stats_response["indices"][index_name]["total"][
                        "store"
                    ]["size_in_bytes"]
                    size_mb = size_bytes / (1024 * 1024)

                    status["indices"][index_name] = {
                        "exists": True,
                        "doc_count": doc_count,
                        "size_mb": round(size_mb, 2),
                    }

                    status["total_docs"] += doc_count
                    status["total_size_mb"] += size_mb
                else:
                    status["indices"][index_name] = {
                        "exists": False,
                        "doc_count": 0,
                        "size_mb": 0,
                    }

            status["total_size_mb"] = round(status["total_size_mb"], 2)
            return status

        except Exception as e:
            return {"connected": True, "error": f"Erro ao obter status: {e}"}

    def clear_cache(self, index_name: Optional[str] = None) -> bool:
        """
        Limpa cache (remove índices)

        Args:
            index_name: Nome do índice específico ou None para todos

        Returns:
            bool: True se limpo com sucesso
        """
        if not self.connected:
            print("❌ Não conectado ao Elasticsearch")
            return False

        try:
            if index_name:
                indices_to_clear = [index_name]
            else:
                indices_to_clear = list(self.indices_config.keys())

            for idx_name in indices_to_clear:
                if self._check_index_exists(idx_name):
                    self.es.indices.delete(index=idx_name)
                    print(f"✅ Índice '{idx_name}' removido")
                else:
                    print(f"ℹ️  Índice '{idx_name}' não existe")

            return True

        except Exception as e:
            print(f"❌ Erro ao limpar cache: {e}")
            return False


# Instância global para uso no notebook
cache_manager = ElasticsearchEmbeddingsCache()


def init_elasticsearch_cache(host="localhost", port=9200) -> bool:
    """
    Inicializa o cache do Elasticsearch

    Args:
        host: Host do Elasticsearch
        port: Porta do Elasticsearch

    Returns:
        bool: True se inicializado com sucesso
    """
    global cache_manager
    cache_manager = ElasticsearchEmbeddingsCache(host=host, port=port)
    return cache_manager.connect()


def get_cache_status() -> Dict[str, Any]:
    """Retorna status do cache"""
    return cache_manager.get_cache_status()


def save_dataset_to_cache(df: pd.DataFrame) -> bool:
    """Salva dataset no cache"""
    return cache_manager.save_dataset(df)


def save_embeddings_to_cache(
    index_name: str,
    embeddings: np.ndarray,
    doc_ids: List[str],
    texts: List[str],
    model_type: str,
    model_version: str = "1.0",
) -> bool:
    """Salva embeddings no cache"""
    return cache_manager.save_embeddings(
        index_name, embeddings, doc_ids, texts, model_type, model_version
    )


def load_embeddings_from_cache(
    index_name: str, doc_ids: List[str]
) -> Optional[np.ndarray]:
    """Carrega embeddings do cache"""
    return cache_manager.load_embeddings(index_name, doc_ids)


def check_embeddings_in_cache(
    index_name: str, doc_ids: List[str]
) -> Tuple[bool, List[str], List[str]]:
    """Verifica se embeddings existem no cache"""
    return cache_manager.check_embeddings_exist(index_name, doc_ids)


def clear_elasticsearch_cache(index_name: Optional[str] = None) -> bool:
    """Limpa cache do Elasticsearch"""
    return cache_manager.clear_cache(index_name)


def validate_embeddings_integrity(
    index_name: str, doc_ids: List[str], texts: List[str]
) -> Tuple[bool, List[str]]:
    """Valida integridade dos embeddings"""
    return cache_manager.validate_embeddings_integrity(index_name, doc_ids, texts)
