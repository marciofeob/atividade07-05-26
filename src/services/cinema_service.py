"""
services/cinema_service.py
Regras de negócio relacionadas à entidade Cinema.
"""

from typing import List, Optional
from src.models.cinema import Cinema
from src.repositories.cinema_repository import CinemaRepository


class CinemaService:

    def __init__(self):
        self._repo = CinemaRepository()

    def cadastrar(self, nome: str, cidade: str, estado: str,
                  endereco: str, capacidade: int) -> Cinema:
        """Valida e cadastra um novo cinema."""
        if capacidade <= 0:
            raise ValueError("A capacidade deve ser maior que zero.")
        if not nome.strip():
            raise ValueError("O nome do cinema não pode ser vazio.")

        cinema = Cinema(
            nome=nome.strip(),
            cidade=cidade.strip(),
            estado=estado.strip().upper(),
            endereco=endereco.strip(),
            capacidade=capacidade,
        )
        return self._repo.salvar(cinema)

    def buscar_por_id(self, cinema_id: int) -> Optional[Cinema]:
        cinema = self._repo.buscar_por_id(cinema_id)
        if not cinema:
            raise ValueError(f"Cinema com ID {cinema_id} não encontrado.")
        return cinema

    def listar_todos(self) -> List[Cinema]:
        return self._repo.listar_todos()
