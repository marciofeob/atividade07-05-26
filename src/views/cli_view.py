"""
views/cli_view.py
Interface de linha de comando (CLI) para o sistema de gestão de cinemas.
Representa a camada View da arquitetura MVC.
"""

from datetime import date
from src.controllers.cinema_controller import CinemaController
from src.controllers.filme_controller import FilmeController
from src.controllers.sessao_controller import SessaoController
from src.controllers.registro_publico_controller import RegistroPublicoController

# Instâncias dos controllers (injetadas na View)
cinema_ctrl = CinemaController()
filme_ctrl = FilmeController()
sessao_ctrl = SessaoController()
registro_ctrl = RegistroPublicoController()


def _linha(char: str = "─", n: int = 55) -> None:
    print(char * n)


def _cabecalho(titulo: str) -> None:
    _linha("═")
    print(f"  🎬  {titulo}")
    _linha("═")


def _input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("  ⚠  Digite um número inteiro válido.")


def _exibir_resultado(resultado: dict) -> None:
    if resultado["sucesso"]:
        dados = resultado["dados"]
        if isinstance(dados, list):
            if not dados:
                print("  (nenhum registro encontrado)")
            for item in dados:
                print(f"  {item}")
        else:
            print(f"  ✔  {dados}")
    else:
        print(f"  ✘  Erro: {resultado['erro']}")


# ─────────────────────────────────────────────────────────────
#  MENUS DE CINEMA
# ─────────────────────────────────────────────────────────────

def menu_cadastrar_cinema() -> None:
    _cabecalho("Cadastrar Cinema")
    nome = input("  Nome do cinema: ").strip()
    cidade = input("  Cidade: ").strip()
    estado = input("  Estado (UF): ").strip()
    endereco = input("  Endereço: ").strip()
    capacidade = _input_int("  Capacidade (nº de lugares): ")
    resultado = cinema_ctrl.cadastrar(nome, cidade, estado, endereco, capacidade)
    _exibir_resultado(resultado)


def menu_listar_cinemas() -> None:
    _cabecalho("Cinemas Cadastrados")
    resultado = cinema_ctrl.listar()
    _exibir_resultado(resultado)


# ─────────────────────────────────────────────────────────────
#  MENUS DE FILME
# ─────────────────────────────────────────────────────────────

def menu_cadastrar_filme() -> None:
    _cabecalho("Cadastrar Filme")
    titulo = input("  Título: ").strip()
    duracao = _input_int("  Duração (em minutos): ")
    genero = input("  Gênero: ").strip()
    diretor = input("  Diretor: ").strip()
    elenco = input("  Elenco (separado por vírgulas): ").strip()
    resultado = filme_ctrl.cadastrar(titulo, duracao, genero, diretor, elenco)
    _exibir_resultado(resultado)


def menu_listar_filmes() -> None:
    _cabecalho("Filmes Cadastrados")
    resultado = filme_ctrl.listar()
    _exibir_resultado(resultado)


def menu_detalhe_filme() -> None:
    _cabecalho("Detalhes do Filme")
    filme_id = _input_int("  ID do filme: ")
    resultado = filme_ctrl.buscar(filme_id)
    if resultado["sucesso"]:
        f = resultado["dados"]
        print(f"\n  Título   : {f.titulo}")
        print(f"  Gênero   : {f.genero}")
        print(f"  Duração  : {f.duracao_min} min")
        print(f"  Diretor  : {f.diretor}")
        print(f"  Elenco   : {f.elenco}")
    else:
        print(f"  ✘  {resultado['erro']}")


# ─────────────────────────────────────────────────────────────
#  MENUS DE SESSÃO
# ─────────────────────────────────────────────────────────────

def menu_criar_sessao() -> None:
    _cabecalho("Criar Sessão")
    print("  Cinemas disponíveis:")
    _exibir_resultado(cinema_ctrl.listar())
    cinema_id = _input_int("\n  ID do cinema: ")

    print("\n  Filmes disponíveis:")
    _exibir_resultado(filme_ctrl.listar())
    filme_id = _input_int("\n  ID do filme: ")

    sala = input("  Sala: ").strip()
    data_hora = input("  Data e hora (YYYY-MM-DD HH:MM): ").strip()
    intervalo = _input_int("  Intervalo após sessão (min, mínimo 15): ")

    resultado = sessao_ctrl.criar(cinema_id, filme_id, data_hora, sala, intervalo)
    _exibir_resultado(resultado)


def menu_listar_sessoes() -> None:
    _cabecalho("Sessões por Cinema")
    cinema_id = _input_int("  ID do cinema: ")
    resultado = sessao_ctrl.listar_por_cinema(cinema_id)
    _exibir_resultado(resultado)


# ─────────────────────────────────────────────────────────────
#  MENUS DE PÚBLICO
# ─────────────────────────────────────────────────────────────

def menu_registrar_publico() -> None:
    _cabecalho("Registrar Público")
    print("  Sessões disponíveis:")
    _exibir_resultado(sessao_ctrl.listar_todas())
    sessao_id = _input_int("\n  ID da sessão: ")
    data = input(f"  Data (YYYY-MM-DD) [Enter para hoje – {date.today()}]: ").strip()
    if not data:
        data = str(date.today())
    quantidade = _input_int("  Quantidade de público: ")
    resultado = registro_ctrl.registrar(sessao_id, data, quantidade)
    _exibir_resultado(resultado)


def menu_relatorio_publico() -> None:
    _cabecalho("Relatório de Público")
    print("  1. Total por Sessão")
    print("  2. Total por Filme")
    print("  3. Total por Cinema")
    opcao = _input_int("\n  Opção: ")

    if opcao == 1:
        sessao_id = _input_int("  ID da sessão: ")
        resultado = registro_ctrl.total_por_sessao(sessao_id)
        if resultado["sucesso"]:
            print(f"\n  📊 Total de público na sessão {sessao_id}: {resultado['dados']:,}")
        else:
            print(f"  ✘  {resultado['erro']}")

    elif opcao == 2:
        filme_id = _input_int("  ID do filme: ")
        resultado = registro_ctrl.total_por_filme(filme_id)
        if resultado["sucesso"]:
            print(f"\n  📊 Total de público do filme {filme_id}: {resultado['dados']:,}")
        else:
            print(f"  ✘  {resultado['erro']}")

    elif opcao == 3:
        cinema_id = _input_int("  ID do cinema: ")
        resultado = registro_ctrl.total_por_cinema(cinema_id)
        if resultado["sucesso"]:
            print(f"\n  📊 Total de público do cinema {cinema_id}: {resultado['dados']:,}")
        else:
            print(f"  ✘  {resultado['erro']}")
    else:
        print("  ⚠  Opção inválida.")


# ─────────────────────────────────────────────────────────────
#  MENU PRINCIPAL
# ─────────────────────────────────────────────────────────────

def menu_principal() -> None:
    opcoes = {
        1: ("Cadastrar Cinema",     menu_cadastrar_cinema),
        2: ("Listar Cinemas",       menu_listar_cinemas),
        3: ("Cadastrar Filme",      menu_cadastrar_filme),
        4: ("Listar Filmes",        menu_listar_filmes),
        5: ("Detalhes de um Filme", menu_detalhe_filme),
        6: ("Criar Sessão",         menu_criar_sessao),
        7: ("Listar Sessões",       menu_listar_sessoes),
        8: ("Registrar Público",    menu_registrar_publico),
        9: ("Relatório de Público", menu_relatorio_publico),
        0: ("Sair",                 None),
    }

    while True:
        print()
        _cabecalho("SISTEMA DE GESTÃO – REDE DE CINEMAS")
        for num, (descricao, _) in opcoes.items():
            print(f"  {num:>2}. {descricao}")
        _linha()

        escolha = _input_int("\n  Escolha uma opção: ")

        if escolha == 0:
            print("\n  Até logo! 🎬\n")
            break
        elif escolha in opcoes:
            print()
            opcoes[escolha][1]()
        else:
            print("  ⚠  Opção inválida. Tente novamente.")
