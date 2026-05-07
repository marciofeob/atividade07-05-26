"""
models/filme.py
Entidade Filme – representa um filme disponível para exibição.
"""

from dataclasses import dataclass


@dataclass
class Filme:
    titulo: str
    duracao_min: int
    genero: str
    diretor: str
    elenco: str
    id: int = None

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.titulo} ({self.duracao_min} min) "
            f"| Gênero: {self.genero} | Diretor: {self.diretor}"
        )
