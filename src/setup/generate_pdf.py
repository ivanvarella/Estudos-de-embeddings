#!/usr/bin/env python3
"""
Script para Gerar PDF do Notebook
=================================

Este script gera um PDF do notebook Jupyter com todas as saídas,
usando nbconvert com configurações otimizadas.

Autor: Sistema de Aulas NLP
Data: 2025
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import argparse

def print_banner():
    """Imprime banner do script"""
    print("📄 GERADOR DE PDF DO NOTEBOOK")
    print("=" * 50)
    print("🎓 Embeddings Avançados e Clustering Semântico")
    print("📚 Material Educacional - Inteligência Computacional")
    print("=" * 50)

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    try:
        import nbconvert
        print("✅ nbconvert disponível")
    except ImportError:
        print("❌ nbconvert não encontrado")
        print("💡 Execute: pip install nbconvert[webpdf]")
        return False
    
    try:
        import jupyter
        print("✅ jupyter disponível")
    except ImportError:
        print("❌ jupyter não encontrado")
        print("💡 Execute: pip install jupyter")
        return False
    
    return True

def check_notebook_exists(notebook_path):
    """Verifica se o notebook ou pasta existe"""
    if not os.path.exists(notebook_path):
        print(f"❌ Caminho não encontrado: {notebook_path}")
        return False
    
    if os.path.isdir(notebook_path):
        # Se for pasta, verificar se tem notebooks
        notebook_files = list(Path(notebook_path).glob("*.ipynb"))
        if not notebook_files:
            print(f"❌ Nenhum notebook encontrado em: {notebook_path}")
            return False
        print(f"✅ Pasta encontrada com {len(notebook_files)} notebooks: {notebook_path}")
        return True
    else:
        print(f"✅ Notebook encontrado: {notebook_path}")
        return True

def generate_pdf(notebook_path, output_dir=".", execute=True, timeout=1800):
    """
    Gera PDF do notebook ou pasta de notebooks
    
    Args:
        notebook_path (str): Caminho para o notebook ou pasta
        output_dir (str): Diretório de saída
        execute (bool): Se deve executar as células
        timeout (int): Timeout em segundos
    """
    
    if os.path.isdir(notebook_path):
        # Se for pasta, processar todos os notebooks
        notebook_files = list(Path(notebook_path).glob("*.ipynb"))
        if not notebook_files:
            print("❌ Nenhum notebook encontrado na pasta")
            return False
        
        print(f"📚 Processando {len(notebook_files)} notebooks...")
        success_count = 0
        
        for notebook_file in notebook_files:
            print(f"\n📄 Processando: {notebook_file.name}")
            if generate_single_pdf(str(notebook_file), output_dir, execute, timeout):
                success_count += 1
        
        print(f"\n✅ Processamento concluído: {success_count}/{len(notebook_files)} notebooks")
        return success_count > 0
    else:
        # Se for arquivo único
        return generate_single_pdf(notebook_path, output_dir, execute, timeout)

def generate_single_pdf(notebook_path, output_dir=".", execute=True, timeout=1800):
    """
    Gera PDF de um notebook específico
    
    Args:
        notebook_path (str): Caminho para o notebook
        output_dir (str): Diretório de saída
        execute (bool): Se deve executar as células
        timeout (int): Timeout em segundos
    """
    
    # Configurar caminhos
    notebook_name = Path(notebook_path).stem
    output_path = os.path.join(output_dir, f"{notebook_name}.pdf")
    
    print(f"📄 Gerando PDF: {output_path}")
    print(f"⏱️  Timeout: {timeout} segundos")
    print(f"🔄 Executar células: {'Sim' if execute else 'Não'}")
    
    # Comando nbconvert
    cmd = [
        "jupyter", "nbconvert",
        "--to", "pdf",
        "--output-dir", output_dir,
        "--allow-errors"
    ]
    
    if execute:
        cmd.append("--execute")
        cmd.extend(["--ExecutePreprocessor.timeout", str(timeout)])
    
    cmd.append(notebook_path)
    
    print(f"🔧 Comando: {' '.join(cmd)}")
    print("⏳ Executando...")
    
    start_time = time.time()
    
    try:
        # Executar comando
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 300  # Timeout adicional para o processo
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ PDF gerado com sucesso!")
            print(f"⏱️  Tempo total: {duration:.1f} segundos")
            print(f"📁 Arquivo: {output_path}")
            
            # Verificar se arquivo foi criado
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"📊 Tamanho: {file_size:.1f} MB")
                return True
            else:
                print("❌ Arquivo PDF não foi criado")
                return False
        else:
            print("❌ Erro ao gerar PDF:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: Processo demorou mais que {timeout} segundos")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def generate_html(notebook_path, output_dir=".", execute=True, timeout=1800):
    """
    Gera HTML do notebook ou pasta de notebooks (alternativa ao PDF)
    
    Args:
        notebook_path (str): Caminho para o notebook ou pasta
        output_dir (str): Diretório de saída
        execute (bool): Se deve executar as células
        timeout (int): Timeout em segundos
    """
    
    if os.path.isdir(notebook_path):
        # Se for pasta, processar todos os notebooks
        notebook_files = list(Path(notebook_path).glob("*.ipynb"))
        if not notebook_files:
            print("❌ Nenhum notebook encontrado na pasta")
            return False
        
        print(f"📚 Processando {len(notebook_files)} notebooks...")
        success_count = 0
        
        for notebook_file in notebook_files:
            print(f"\n🌐 Processando: {notebook_file.name}")
            if generate_single_html(str(notebook_file), output_dir, execute, timeout):
                success_count += 1
        
        print(f"\n✅ Processamento concluído: {success_count}/{len(notebook_files)} notebooks")
        return success_count > 0
    else:
        # Se for arquivo único
        return generate_single_html(notebook_path, output_dir, execute, timeout)

def generate_single_html(notebook_path, output_dir=".", execute=True, timeout=1800):
    """
    Gera HTML de um notebook específico
    
    Args:
        notebook_path (str): Caminho para o notebook
        output_dir (str): Diretório de saída
        execute (bool): Se deve executar as células
        timeout (int): Timeout em segundos
    """
    
    # Configurar caminhos
    notebook_name = Path(notebook_path).stem
    output_path = os.path.join(output_dir, f"{notebook_name}.html")
    
    print(f"🌐 Gerando HTML: {output_path}")
    
    # Comando nbconvert para HTML
    cmd = [
        "jupyter", "nbconvert",
        "--to", "html",
        "--output-dir", output_dir,
        "--allow-errors"
    ]
    
    if execute:
        cmd.append("--execute")
        cmd.extend(["--ExecutePreprocessor.timeout", str(timeout)])
    
    cmd.append(notebook_path)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 300)
        
        if result.returncode == 0:
            print(f"✅ HTML gerado com sucesso!")
            print(f"📁 Arquivo: {output_path}")
            return True
        else:
            print("❌ Erro ao gerar HTML:")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Gerar PDF/HTML do notebook")
    parser.add_argument("--notebook", "-n", default="src/",
                       help="Caminho para o notebook ou pasta (padrão: src/)")
    parser.add_argument("--output", "-o", default=".",
                       help="Diretório de saída (padrão: diretório atual)")
    parser.add_argument("--no-execute", action="store_true",
                       help="Não executar células (apenas converter)")
    parser.add_argument("--timeout", "-t", type=int, default=1800,
                       help="Timeout em segundos (padrão: 1800)")
    parser.add_argument("--html", action="store_true",
                       help="Gerar HTML em vez de PDF")
    parser.add_argument("--both", action="store_true",
                       help="Gerar tanto PDF quanto HTML")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar notebook
    if not check_notebook_exists(args.notebook):
        sys.exit(1)
    
    # Criar diretório de saída se não existir
    os.makedirs(args.output, exist_ok=True)
    
    success = False
    
    if args.html or args.both:
        print("\n🌐 GERANDO HTML")
        print("-" * 30)
        success = generate_html(args.notebook, args.output, not args.no_execute, args.timeout)
    
    if not args.html or args.both:
        print("\n📄 GERANDO PDF")
        print("-" * 30)
        success = generate_pdf(args.notebook, args.output, not args.no_execute, args.timeout)
    
    if success:
        print("\n🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!")
        print("💡 Dicas:")
        print("   • PDF: Melhor para impressão e compartilhamento")
        print("   • HTML: Melhor para visualização online")
        print("   • Use --no-execute para conversão rápida (sem saídas)")
    else:
        print("\n❌ FALHA NA CONVERSÃO")
        print("💡 Soluções:")
        print("   • Verifique se o notebook executa sem erros")
        print("   • Aumente o timeout com --timeout 3600")
        print("   • Use --no-execute para pular execução")
        print("   • Tente gerar HTML com --html")
        sys.exit(1)

if __name__ == "__main__":
    main()
