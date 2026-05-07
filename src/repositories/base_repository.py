"""
repositories/base_repository.py
Classe base para os repositórios fornecerem conexão com o banco de dados.
"""
from src.database.db import get_connection

class BaseRepository:
    """Fornece a conexão SQLite para as classes filhas."""
    
    def get_connection(self):
        return get_connection()