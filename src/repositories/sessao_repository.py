"""
repositories/sessao_repository.py
Operações de persistência para a entidade Sessão.
"""

from typing import List, Optional
from src.models.sessao import Sessao
from src.repositories.base_repository import BaseRepository


class SessaoRepository(BaseRepository):

    def salvar(self, sessao: Sessao) -> Sessao:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sessoes (cinema_id, filme_id, data_hora, sala, intervalo_min)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sessao.cinema_id, sessao.filme_id, sessao.data_hora,
             sessao.sala, sessao.intervalo_min),
        )
        conn.commit()
        sessao.id = cursor.lastrowid
        conn.close()
        return sessao

    def buscar_por_id(self, sessao_id: int) -> Optional[Sessao]:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM sessoes WHERE id = ?", (sessao_id,)
        ).fetchone()
        conn.close()
        return self._row_to_sessao(row) if row else None

    def buscar_por_sala(self, cinema_id: int, sala: str) -> List[Sessao]:
        """Retorna todas as sessões de uma sala específica de um cinema."""
        conn = self._get_conn()
        rows = conn.execute(
            """
            SELECT * FROM sessoes
            WHERE cinema_id = ? AND sala = ?
            ORDER BY data_hora
            """,
            (cinema_id, sala),
        ).fetchall()
        conn.close()
        return [self._row_to_sessao(r) for r in rows]

    def listar_por_cinema(self, cinema_id: int) -> List[Sessao]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM sessoes WHERE cinema_id = ? ORDER BY data_hora",
            (cinema_id,),
        ).fetchall()
        conn.close()
        return [self._row_to_sessao(r) for r in rows]

    def listar_todos(self) -> List[Sessao]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM sessoes ORDER BY data_hora"
        ).fetchall()
        conn.close()
        return [self._row_to_sessao(r) for r in rows]

    @staticmethod
    def _row_to_sessao(row) -> Sessao:
        return Sessao(
            id=row["id"],
            cinema_id=row["cinema_id"],
            filme_id=row["filme_id"],
            data_hora=row["data_hora"],
            sala=row["sala"],
            intervalo_min=row["intervalo_min"],
        )
