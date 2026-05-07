"""
controllers/registro_publico_controller.py
Orquestra as operações relacionadas a RegistroPublico entre View e Service.
"""

from src.services.registro_publico_service import RegistroPublicoService


class RegistroPublicoController:

    def __init__(self):
        self._service = RegistroPublicoService()

    def registrar(self, sessao_id: int, data: str, quantidade: int) -> dict:
        try:
            registro = self._service.registrar(sessao_id, data, quantidade)
            return {"sucesso": True, "dados": registro}
        except ValueError as e:
            return {"sucesso": False, "erro": str(e)}

    def total_por_sessao(self, sessao_id: int) -> dict:
        try:
            total = self._service.total_por_sessao(sessao_id)
            return {"sucesso": True, "dados": total}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}

    def total_por_filme(self, filme_id: int) -> dict:
        try:
            total = self._service.total_por_filme(filme_id)
            return {"sucesso": True, "dados": total}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}

    def total_por_cinema(self, cinema_id: int) -> dict:
        try:
            total = self._service.total_por_cinema(cinema_id)
            return {"sucesso": True, "dados": total}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}
