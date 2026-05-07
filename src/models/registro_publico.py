"""
models/registro_publico.py
Entidade RegistroPublico – representa o público de uma sessão em determinada data.
"""

from dataclasses import dataclass


@dataclass
class RegistroPublico:
    sessao_id: int
    data: str           # formato ISO: "YYYY-MM-DD"
    quantidade_publico: int
    id: int = None

    def __str__(self) -> str:
        return (
            f"[{self.id}] Sessão ID: {self.sessao_id} "
            f"| Data: {self.data} | Público: {self.quantidade_publico}"
        )
