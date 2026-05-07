"""
repositories/filme_repository.py
Operações de persistência para a entidade Filme.
"""

from typing import List, Optional
from src.models.filme import Filme
from src.repositories.base_repository import BaseRepository


class FilmeRepository(BaseRepository):

    def salvar(self, filme: Filme) -> Filme:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO filmes (titulo, duracao_min, genero, diretor, elenco)
            VALUES (?, ?, ?, ?, ?)
            """,
            (filme.titulo, filme.duracao_min, filme.genero,
             filme.diretor, filme.elenco),
        )
        conn.commit()
        filme.id = cursor.lastrowid
        conn.close()
        return filme

    def buscar_por_id(self, filme_id: int) -> Optional[Filme]:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM filmes WHERE id = ?", (filme_id,)
        ).fetchone()
        conn.close()
        return self._row_to_filme(row) if row else None

    def listar_todos(self) -> List[Filme]:
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM filmes ORDER BY titulo").fetchall()
        conn.close()
        return [self._row_to_filme(r) for r in rows]

    @staticmethod
    def _row_to_filme(row) -> Filme:
        return Filme(
            id=row["id"],
            titulo=row["titulo"],
            duracao_min=row["duracao_min"],
            genero=row["genero"],
            diretor=row["diretor"],
            elenco=row["elenco"],
        )
