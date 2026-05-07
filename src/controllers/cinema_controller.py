"""
controllers/cinema_controller.py
Orquestra as operações relacionadas a Cinema entre View e Service.
"""

from src.services.cinema_service import CinemaService


class CinemaController:

    def __init__(self):
        self._service = CinemaService()

    def cadastrar(self, nome: str, cidade: str, estado: str,
                  endereco: str, capacidade: int) -> dict:
        try:
            cinema = self._service.cadastrar(nome, cidade, estado, endereco, capacidade)
            return {"sucesso": True, "dados": cinema}
        except ValueError as e:
            return {"sucesso": False, "erro": str(e)}

    def listar(self) -> dict:
        try:
            cinemas = self._service.listar_todos()
            return {"sucesso": True, "dados": cinemas}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}

    def buscar(self, cinema_id: int) -> dict:
        try:
            cinema = self._service.buscar_por_id(cinema_id)
            return {"sucesso": True, "dados": cinema}
        except ValueError as e:
            return {"sucesso": False, "erro": str(e)}
