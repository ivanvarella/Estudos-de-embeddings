#!/usr/bin/env python3
"""
Script de inicialização rápida para o notebook Seção 5.1
Este script configura o ambiente e inicia o Jupyter Notebook automaticamente.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_environment():
    """Verifica se o ambiente está configurado"""
    print("🔍 Verificando ambiente...")
    
    # Verificar se o script de teste existe
    test_script = Path(__file__).parent / "test_environment.py"
    if not test_script.exists():
        print("❌ Script de teste não encontrado")
        return False
    
    # Executar teste
    try:
        result = subprocess.run([sys.executable, str(test_script)], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ambiente verificado com sucesso")
            return True
        else:
            print("⚠️  Ambiente com problemas, mas continuando...")
            return True
    except Exception as e:
        print(f"⚠️  Erro ao verificar ambiente: {e}")
        return True

def start_jupyter():
    """Inicia o Jupyter Notebook"""
    print("🚀 Iniciando Jupyter Notebook...")
    
    notebook_path = Path(__file__).parent.parent / "Seção5.1_Embeddings.ipynb"
    
    if not notebook_path.exists():
        print("❌ Notebook não encontrado")
        return False
    
    try:
        # Iniciar Jupyter com o notebook específico
        subprocess.run([
            "jupyter", "notebook", 
            str(notebook_path),
            "--no-browser",
            "--port=8888"
        ])
        return True
    except FileNotFoundError:
        print("❌ Jupyter Notebook não encontrado")
        print("Instale com: pip install jupyter")
        return False
    except KeyboardInterrupt:
        print("\n👋 Jupyter Notebook encerrado")
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar Jupyter: {e}")
        return False

def show_instructions():
    """Mostra instruções para o usuário"""
    print("\n" + "=" * 60)
    print("📚 INSTRUÇÕES PARA O NOTEBOOK")
    print("=" * 60)
    print("1. Execute as células em ordem sequencial")
    print("2. Aguarde o carregamento dos modelos (pode demorar)")
    print("3. Para Elasticsearch: docker-compose up -d")
    print("4. Para OpenAI: configure sua chave no notebook")
    print("\n🎯 FUNCIONALIDADES PRINCIPAIS:")
    print("• Embeddings: Word2Vec, BERT, Sentence-BERT, OpenAI")
    print("• Clustering: K-Means, DBSCAN, HDBSCAN")
    print("• Visualização: PCA, t-SNE, UMAP")
    print("• Busca semântica: Elasticsearch")
    print("• Classificação: Upload de textos personalizados")
    print("\n💡 DICAS:")
    print("• Use Ctrl+C para interromper execução")
    print("• Salve o notebook regularmente")
    print("• Verifique os logs em caso de erro")
    print("=" * 60)

def main():
    """Função principal"""
    print("🎓 INICIANDO SEÇÃO 5.1 - EMBEDDINGS AVANÇADOS")
    print("=" * 60)
    
    # Verificar ambiente
    if not check_environment():
        print("❌ Ambiente não configurado. Execute setup_environment.py primeiro")
        return 1
    
    # Mostrar instruções
    show_instructions()
    
    # Perguntar se quer continuar
    try:
        response = input("\n▶️  Iniciar Jupyter Notebook? (s/N): ").strip().lower()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("👋 Operação cancelada")
            return 0
    except KeyboardInterrupt:
        print("\n👋 Operação cancelada")
        return 0
    
    # Iniciar Jupyter
    if start_jupyter():
        print("✅ Jupyter Notebook iniciado com sucesso!")
        return 0
    else:
        print("❌ Falha ao iniciar Jupyter Notebook")
        return 1

if __name__ == "__main__":
    sys.exit(main())
