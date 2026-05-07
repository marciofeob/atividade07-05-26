"""
services/registro_publico_service.py
Regras de negócio para registro de público.

Regras aplicadas:
  RN03 – Público não pode exceder a capacidade do cinema.
"""

from src.models.registro_publico import RegistroPublico
from src.repositories.registro_publico_repository import RegistroPublicoRepository
from src.repositories.sessao_repository import SessaoRepository
from src.repositories.cinema_repository import CinemaRepository


class RegistroPublicoService:

    def __init__(self):
        self._repo = RegistroPublicoRepository()
        self._sessao_repo = SessaoRepository()
        self._cinema_repo = CinemaRepository()

    def registrar(self, sessao_id: int, data: str, quantidade: int) -> RegistroPublico:
        """Registra o público de uma sessão com validação de capacidade (RN03)."""
        if quantidade < 0:
            raise ValueError("A quantidade de público não pode ser negativa.")

        sessao = self._sessao_repo.buscar_por_id(sessao_id)
        if not sessao:
            raise ValueError(f"Sessão ID {sessao_id} não encontrada.")

        cinema = self._cinema_repo.buscar_por_id(sessao.cinema_id)
        if quantidade > cinema.capacidade:
            raise ValueError(
                f"Público informado ({quantidade}) excede a capacidade "
                f"do cinema '{cinema.nome}' ({cinema.capacidade} lugares)."
            )

        registro = RegistroPublico(
            sessao_id=sessao_id,
            data=data,
            quantidade_publico=quantidade,
        )
        return self._repo.salvar(registro)

    def total_por_sessao(self, sessao_id: int) -> int:
        return self._repo.total_por_sessao(sessao_id)

    def total_por_filme(self, filme_id: int) -> int:
        return self._repo.total_por_filme(filme_id)

    def total_por_cinema(self, cinema_id: int) -> int:
        return self._repo.total_por_cinema(cinema_id)
