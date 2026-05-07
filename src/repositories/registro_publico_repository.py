"""
repositories/registro_publico_repository.py
Operações de persistência para a entidade RegistroPublico.
"""

from typing import List, Optional
from src.models.registro_publico import RegistroPublico
from src.repositories.base_repository import BaseRepository


class RegistroPublicoRepository(BaseRepository):

    def salvar(self, registro: RegistroPublico) -> RegistroPublico:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO registros_publico (sessao_id, data, quantidade_publico)
            VALUES (?, ?, ?)
            """,
            (registro.sessao_id, registro.data, registro.quantidade_publico),
        )
        conn.commit()
        registro.id = cursor.lastrowid
        conn.close()
        return registro

    def buscar_por_sessao(self, sessao_id: int) -> List[RegistroPublico]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM registros_publico WHERE sessao_id = ? ORDER BY data",
            (sessao_id,),
        ).fetchall()
        conn.close()
        return [self._row_to_registro(r) for r in rows]

    def total_por_sessao(self, sessao_id: int) -> int:
        """Retorna o total de público de uma sessão."""
        conn = self._get_conn()
        result = conn.execute(
            "SELECT COALESCE(SUM(quantidade_publico), 0) FROM registros_publico WHERE sessao_id = ?",
            (sessao_id,),
        ).fetchone()
        conn.close()
        return result[0]

    def total_por_filme(self, filme_id: int) -> int:
        """Retorna o total de público de um filme em toda a rede."""
        conn = self._get_conn()
        result = conn.execute(
            """
            SELECT COALESCE(SUM(rp.quantidade_publico), 0)
            FROM registros_publico rp
            JOIN sessoes s ON s.id = rp.sessao_id
            WHERE s.filme_id = ?
            """,
            (filme_id,),
        ).fetchone()
        conn.close()
        return result[0]

    def total_por_cinema(self, cinema_id: int) -> int:
        """Retorna o total de público de um cinema em toda a sua história."""
        conn = self._get_conn()
        result = conn.execute(
            """
            SELECT COALESCE(SUM(rp.quantidade_publico), 0)
            FROM registros_publico rp
            JOIN sessoes s ON s.id = rp.sessao_id
            WHERE s.cinema_id = ?
            """,
            (cinema_id,),
        ).fetchone()
        conn.close()
        return result[0]

    @staticmethod
    def _row_to_registro(row) -> RegistroPublico:
        return RegistroPublico(
            id=row["id"],
            sessao_id=row["sessao_id"],
            data=row["data"],
            quantidade_publico=row["quantidade_publico"],
        )
