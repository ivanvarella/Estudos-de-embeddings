#!/usr/bin/env python3
"""
Script de configuração do ambiente para Seção 5.1 - Embeddings Avançados
Execute este script antes de rodar o notebook para verificar dependências e configurar o ambiente.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(
            "❌ Python 3.8+ é necessário. Versão atual:",
            f"{version.major}.{version.minor}",
        )
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True


def install_requirements():
    """Instala dependências do requirements.txt"""
    requirements_file = Path(__file__).parent.parent.parent / "requirements.txt"

    if not requirements_file.exists():
        print("❌ Arquivo requirements.txt não encontrado")
        return False

    print("🔄 Instalando dependências...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        )
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False


def check_docker():
    """Verifica se Docker está disponível"""
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
        print("✅ Docker e Docker Compose disponíveis")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Docker não encontrado. Elasticsearch não estará disponível")
        print("   Instale Docker Desktop para usar funcionalidades de busca semântica")
        return False


def create_directories():
    """Cria diretórios necessários"""
    directories = ["data", "models", "results", "logs"]

    for dir_name in directories:
        dir_path = Path(__file__).parent.parent / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"📁 Diretório criado: {dir_name}")


def check_openai_key():
    """Verifica se a chave da OpenAI está configurada"""
    # Carregar variáveis do .env se existir
    env_paths = [
        Path(__file__).parent / ".env",  # setup/.env
        Path(__file__).parent.parent / ".env",  # raiz/.env
    ]

    for env_file in env_paths:
        if env_file.exists():
            try:
                from dotenv import load_dotenv

                load_dotenv(env_file)
                break
            except ImportError:
                # Se dotenv não estiver disponível, carregar manualmente
                with open(env_file, "r") as f:
                    for line in f:
                        if line.strip() and not line.startswith("#"):
                            key, value = line.strip().split("=", 1)
                            os.environ[key] = value
                break

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "sk-your-openai-key-here":
        print("✅ Chave da OpenAI configurada")
        return True
    else:
        print("⚠️  Chave da OpenAI não encontrada")
        print("   Configure com: export OPENAI_API_KEY='sua-chave-aqui'")
        print("   Ou adicione no notebook: openai.api_key = 'sua-chave-aqui'")
        return False


def main():
    """Função principal de configuração"""
    print("🚀 CONFIGURAÇÃO DO AMBIENTE - SEÇÃO 5.1")
    print("=" * 50)

    # Verificar Python
    if not check_python_version():
        sys.exit(1)

    # Instalar dependências
    if not install_requirements():
        print("❌ Falha na instalação de dependências")
        sys.exit(1)

    # Verificar Docker
    docker_available = check_docker()

    # Criar diretórios
    create_directories()

    # Verificar OpenAI
    openai_configured = check_openai_key()

    print("\n" + "=" * 50)
    print("📋 RESUMO DA CONFIGURAÇÃO")
    print("=" * 50)
    print("✅ Python: OK")
    print("✅ Dependências: Instaladas")
    print(
        f"{'✅' if docker_available else '⚠️ '} Docker: {'Disponível' if docker_available else 'Não disponível'}"
    )
    print(
        f"{'✅' if openai_configured else '⚠️ '} OpenAI: {'Configurado' if openai_configured else 'Não configurado'}"
    )

    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Execute os notebooks: jupyter notebook src/")
    print("   • Part1: Preparação e Dataset")
    print("   • Part2: Embeddings Locais")
    print("   • Part3: Embeddings OpenAI")
    print("   • Part4: Análise Comparativa")
    print("   • Part5: Clustering e ML")

    if docker_available:
        print("2. Para Elasticsearch: docker-compose up -d")
        print("3. Acesse Kibana: http://localhost:5601")

    if not openai_configured:
        print("4. Configure sua chave da OpenAI no notebook")

    print("\n✅ Ambiente configurado com sucesso!")


if __name__ == "__main__":
    main()
