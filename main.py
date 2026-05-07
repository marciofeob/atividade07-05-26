"""
main.py
Ponto de entrada do sistema de gestão de rede de cinemas.
Inicializa o banco de dados e inicia a interface CLI.
"""

import sys
import os

# Garante que o diretório raiz esteja no path para imports absolutos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db import inicializar_banco
from src.views.cli_view import menu_principal


def main() -> None:
    inicializar_banco()
    menu_principal()


if __name__ == "__main__":
    main()
