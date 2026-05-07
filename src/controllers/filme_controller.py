"""
controllers/filme_controller.py
Orquestra as operações relacionadas a Filme entre View e Service.
"""

from src.services.filme_service import FilmeService


class FilmeController:

    def __init__(self):
        self._service = FilmeService()

    def cadastrar(self, titulo: str, duracao_min: int, genero: str,
                  diretor: str, elenco: str) -> dict:
        try:
            filme = self._service.cadastrar(titulo, duracao_min, genero, diretor, elenco)
            return {"sucesso": True, "dados": filme}
        except ValueError as e:
            return {"sucesso": False, "erro": str(e)}

    def listar(self) -> dict:
        try:
            filmes = self._service.listar_todos()
            return {"sucesso": True, "dados": filmes}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}

    def buscar(self, filme_id: int) -> dict:
        try:
            filme = self._service.buscar_por_id(filme_id)
            return {"sucesso": True, "dados": filme}
        except ValueError as e:
            return {"sucesso": False, "erro": str(e)}
