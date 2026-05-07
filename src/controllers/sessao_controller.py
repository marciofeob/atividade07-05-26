"""
controllers/sessao_controller.py
Orquestra as operações relacionadas a Sessão entre View e Service.
"""

from src.services.sessao_service import SessaoService


class SessaoController:

    def __init__(self):
        self._service = SessaoService()

    def criar(self, cinema_id: int, filme_id: int,
              data_hora: str, sala: str, intervalo_min: int = 15) -> dict:
        try:
            sessao = self._service.criar(cinema_id, filme_id, data_hora, sala, intervalo_min)
            return {"sucesso": True, "dados": sessao}
        except ValueError as e:
            return {"sucesso": False, "erro": str(e)}

    def listar_por_cinema(self, cinema_id: int) -> dict:
        try:
            sessoes = self._service.listar_por_cinema(cinema_id)
            return {"sucesso": True, "dados": sessoes}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}

    def listar_todas(self) -> dict:
        try:
            sessoes = self._service.listar_todas()
            return {"sucesso": True, "dados": sessoes}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}
