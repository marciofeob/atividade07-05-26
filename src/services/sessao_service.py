"""
services/sessao_service.py
Regras de negócio relacionadas à entidade Sessão.

Regras aplicadas:
  RN01 – Sem conflito de horário na mesma sala/cinema.
  RN02 – Intervalo mínimo de 15 min entre sessões na mesma sala.
  RN04 – Fim da sessão = data_hora + duracao_min do filme.
"""

from datetime import datetime, timedelta
from typing import List

from src.models.sessao import Sessao
from src.repositories.sessao_repository import SessaoRepository
from src.repositories.filme_repository import FilmeRepository
from src.repositories.cinema_repository import CinemaRepository

INTERVALO_MINIMO_MIN = 15


class SessaoService:

    def __init__(self):
        self._repo = SessaoRepository()
        self._filme_repo = FilmeRepository()
        self._cinema_repo = CinemaRepository()

    def criar(self, cinema_id: int, filme_id: int,
              data_hora: str, sala: str, intervalo_min: int = 15) -> Sessao:
        """Cria uma sessão aplicando todas as regras de negócio."""

        # Verifica existência das dependências
        cinema = self._cinema_repo.buscar_por_id(cinema_id)
        if not cinema:
            raise ValueError(f"Cinema ID {cinema_id} não encontrado.")

        filme = self._filme_repo.buscar_por_id(filme_id)
        if not filme:
            raise ValueError(f"Filme ID {filme_id} não encontrado.")

        if intervalo_min < INTERVALO_MINIMO_MIN:
            raise ValueError(
                f"O intervalo mínimo entre sessões é de {INTERVALO_MINIMO_MIN} minutos."
            )

        nova_inicio = datetime.fromisoformat(data_hora)
        nova_fim = nova_inicio + timedelta(minutes=filme.duracao_min)

        # RN01 e RN02 – verificar conflitos na mesma sala
        sessoes_existentes = self._repo.buscar_por_sala(cinema_id, sala)
        for sessao in sessoes_existentes:
            filme_existente = self._filme_repo.buscar_por_id(sessao.filme_id)
            existente_inicio = sessao.get_datetime()
            existente_fim = existente_inicio + timedelta(minutes=filme_existente.duracao_min)

            # Janela com intervalo obrigatório
            existente_fim_com_intervalo = existente_fim + timedelta(minutes=sessao.intervalo_min)
            nova_fim_com_intervalo = nova_fim + timedelta(minutes=intervalo_min)

            # Há sobreposição se uma sessão começa antes do fim+intervalo da outra
            if nova_inicio < existente_fim_com_intervalo and nova_fim_com_intervalo > existente_inicio:
                raise ValueError(
                    f"Conflito de horário na sala '{sala}': "
                    f"sessão existente das {existente_inicio.strftime('%H:%M')} "
                    f"às {existente_fim.strftime('%H:%M')} "
                    f"(com intervalo até {existente_fim_com_intervalo.strftime('%H:%M')})."
                )

        sessao = Sessao(
            cinema_id=cinema_id,
            filme_id=filme_id,
            data_hora=data_hora,
            sala=sala,
            intervalo_min=intervalo_min,
        )
        return self._repo.salvar(sessao)

    def buscar_por_id(self, sessao_id: int) -> Sessao:
        sessao = self._repo.buscar_por_id(sessao_id)
        if not sessao:
            raise ValueError(f"Sessão ID {sessao_id} não encontrada.")
        return sessao

    def listar_por_cinema(self, cinema_id: int) -> List[Sessao]:
        return self._repo.listar_por_cinema(cinema_id)

    def listar_todas(self) -> List[Sessao]:
        return self._repo.listar_todos()
