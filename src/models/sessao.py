"""
models/sessao.py
Entidade Sessão – representa uma exibição de filme em um cinema.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sessao:
    cinema_id: int
    filme_id: int
    data_hora: str        # formato ISO: "YYYY-MM-DD HH:MM"
    sala: str
    intervalo_min: int = 15
    id: int = None

    def get_datetime(self) -> datetime:
        return datetime.fromisoformat(self.data_hora)

    def __str__(self) -> str:
        return (
            f"[{self.id}] Sala {self.sala} | {self.data_hora} "
            f"| Cinema ID: {self.cinema_id} | Filme ID: {self.filme_id}"
        )
