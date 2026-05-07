"""
services/filme_service.py
Regras de negócio relacionadas à entidade Filme.
"""

from typing import List, Optional
from src.models.filme import Filme
from src.repositories.filme_repository import FilmeRepository


class FilmeService:

    def __init__(self):
        self._repo = FilmeRepository()

    def cadastrar(self, titulo: str, duracao_min: int, genero: str,
                  diretor: str, elenco: str) -> Filme:
        if duracao_min <= 0:
            raise ValueError("A duração do filme deve ser maior que zero.")
        if not titulo.strip():
            raise ValueError("O título do filme não pode ser vazio.")

        filme = Filme(
            titulo=titulo.strip(),
            duracao_min=duracao_min,
            genero=genero.strip(),
            diretor=diretor.strip(),
            elenco=elenco.strip(),
        )
        return self._repo.salvar(filme)

    def buscar_por_id(self, filme_id: int) -> Optional[Filme]:
        filme = self._repo.buscar_por_id(filme_id)
        if not filme:
            raise ValueError(f"Filme com ID {filme_id} não encontrado.")
        return filme

    def listar_todos(self) -> List[Filme]:
        return self._repo.listar_todos()
