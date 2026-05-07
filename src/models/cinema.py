"""
models/cinema.py
Entidade Cinema – representa uma unidade da rede de cinemas.
"""

from dataclasses import dataclass


@dataclass
class Cinema:
    nome: str
    cidade: str
    estado: str
    endereco: str
    capacidade: int
    id: int = None

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.nome} – {self.cidade}/{self.estado} "
            f"| Capacidade: {self.capacidade} | Endereço: {self.endereco}"
        )
