#!/usr/bin/env python3
"""
Script de verificação de problemas críticos no projeto
Execute este script para identificar problemas conhecidos antes de executar o notebook.
"""

import os
import re
import sys
from pathlib import Path

def check_openai_api_consistency():
    """Verifica consistência da API da OpenAI"""
    print("🔍 Verificando consistência da API da OpenAI...")
    
    notebook_path = Path(__file__).parent.parent / "Seção5.1_Embeddings.ipynb"
    
    if not notebook_path.exists():
        print("❌ Notebook não encontrado")
        return False
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se usa API v0.x (deprecated)
    if 'openai.api_key' in content:
        print("❌ PROBLEMA CRÍTICO: Código usa API v0.x (deprecated)")
        print("   Solução: Use 'client = openai.OpenAI(api_key=\"...\")'")
        return False
    
    # Verificar se usa API v1.x
    if 'openai.OpenAI' in content:
        print("✅ API da OpenAI configurada corretamente (v1.x)")
        return True
    
    print("⚠️  API da OpenAI não configurada")
    return True

def check_undefined_functions():
    """Verifica se há funções usadas antes de serem definidas"""
    print("🔍 Verificando funções não definidas...")
    
    notebook_path = Path(__file__).parent.parent / "Seção5.1_Embeddings.ipynb"
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se classifier.best_combination é usado antes de classifier = TextClassifier
    classifier_usage = content.find('classifier.best_combination')
    classifier_definition = content.find('classifier = TextClassifier')
    
    if classifier_usage != -1:
        if classifier_definition == -1:
            print("❌ PROBLEMA CRÍTICO: classifier não é instanciado mas é usado")
            print("   Solução: Instancie classifier = TextClassifier(...)")
            return False
        elif classifier_usage < classifier_definition:
            print("❌ PROBLEMA CRÍTICO: classifier.best_combination usado antes de classifier ser definido")
            print("   Solução: Defina classifier antes de usar")
            return False
    
    print("✅ Nenhum uso indevido de funções não definidas")
    return True

def check_requirements_consistency():
    """Verifica consistência do requirements.txt"""
    print("🔍 Verificando requirements.txt...")
    
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_path.exists():
        print("❌ requirements.txt não encontrado")
        return False
    
    with open(requirements_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se pathlib2 está presente (desnecessário)
    if 'pathlib2' in content:
        print("❌ PROBLEMA: pathlib2 é desnecessário")
        print("   Solução: Remover pathlib2 do requirements.txt")
        return False
    
    # Verificar versões muito antigas
    if 'numpy>=1.21.0' in content:
        print("⚠️  VERSÃO ANTIGA: numpy>=1.21.0 é muito antigo")
        print("   Solução: Atualizar para numpy>=1.24.0")
        return False
    
    print("✅ requirements.txt está correto")
    return True

def check_docker_compose():
    """Verifica configuração do Docker Compose"""
    print("🔍 Verificando docker-compose.yml...")
    
    docker_path = Path(__file__).parent.parent / "docker-compose.yml"
    
    if not docker_path.exists():
        print("❌ docker-compose.yml não encontrado")
        return False
    
    with open(docker_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se tem configurações de rede
    if 'networks:' in content:
        print("✅ Docker Compose configurado corretamente")
        return True
    
    print("⚠️  Docker Compose pode ter problemas de configuração")
    return True

def check_makefile_consistency():
    """Verifica consistência do Makefile"""
    print("🔍 Verificando Makefile...")
    
    makefile_path = Path(__file__).parent.parent / "Makefile"
    
    if not makefile_path.exists():
        print("❌ Makefile não encontrado")
        return False
    
    with open(makefile_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se tem comando docs
    if 'docs:' in content:
        print("✅ Makefile tem comando docs")
        return True
    
    print("⚠️  Makefile pode estar incompleto")
    return True

def main():
    """Função principal de verificação"""
    print("🚨 VERIFICAÇÃO DE PROBLEMAS CRÍTICOS")
    print("=" * 50)
    
    checks = [
        ("API da OpenAI", check_openai_api_consistency),
        ("Funções não definidas", check_undefined_functions),
        ("Requirements.txt", check_requirements_consistency),
        ("Docker Compose", check_docker_compose),
        ("Makefile", check_makefile_consistency)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Erro ao verificar {check_name}: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{check_name:<20}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} verificações passaram")
    
    if passed == total:
        print("\n🎉 Todas as verificações passaram! O projeto está pronto.")
        return 0
    elif passed >= total - 1:
        print("\n⚠️  Projeto com problemas menores. Pode executar com cautela.")
        return 1
    else:
        print("\n❌ Projeto com problemas críticos. Corrija antes de executar.")
        print("\n📖 Leia CORREÇÕES_CRÍTICAS.md para soluções detalhadas.")
        return 2

if __name__ == "__main__":
    sys.exit(main())
