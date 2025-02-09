# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:11:06 2025

@author: PC
"""

import pkg_resources
import ast
import os
import subprocess

def extract_imports(file_path):
    """Extrai módulos importados de um script Python."""
    imports = set()
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    return imports

def get_installed_packages():
    """Obtém os pacotes instalados com suas versões."""
    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    return installed

def generate_requirements(scripts, output_file="requirements.txt"):
    """Gera um arquivo requirements.txt com as dependências exatas."""
    all_imports = set()
    for script in scripts:
        all_imports.update(extract_imports(script))
    
    installed_packages = get_installed_packages()
    
    with open(output_file, "w", encoding="utf-8") as f:
        for package in sorted(all_imports):
            if package in installed_packages:
                f.write(f"{package}=={installed_packages[package]}\n")
    
    print(f"Arquivo {output_file} gerado com sucesso!")

if __name__ == "__main__":
    scripts = ["Front.py", "data_viz_complex.py", "data_viz.py"]  # Adicione os scripts desejados
    generate_requirements(scripts)
