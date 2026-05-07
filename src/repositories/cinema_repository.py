"""
repositories/cinema_repository.py
Operações de persistência para a entidade Cinema.
"""

from typing import List, Optional
from src.models.cinema import Cinema
from src.repositories.base_repository import BaseRepository


class CinemaRepository(BaseRepository):

    def salvar(self, cinema: Cinema) -> Cinema:
        """Insere um novo cinema e retorna o objeto com o ID gerado."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cinemas (nome, cidade, estado, endereco, capacidade)
            VALUES (?, ?, ?, ?, ?)
            """,
            (cinema.nome, cinema.cidade, cinema.estado,
             cinema.endereco, cinema.capacidade),
        )
        conn.commit()
        cinema.id = cursor.lastrowid
        conn.close()
        return cinema

    def buscar_por_id(self, cinema_id: int) -> Optional[Cinema]:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM cinemas WHERE id = ?", (cinema_id,)
        ).fetchone()
        conn.close()
        return self._row_to_cinema(row) if row else None

    def listar_todos(self) -> List[Cinema]:
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM cinemas ORDER BY nome").fetchall()
        conn.close()
        return [self._row_to_cinema(r) for r in rows]

    @staticmethod
    def _row_to_cinema(row) -> Cinema:
        return Cinema(
            id=row["id"],
            nome=row["nome"],
            cidade=row["cidade"],
            estado=row["estado"],
            endereco=row["endereco"],
            capacidade=row["capacidade"],
        )
