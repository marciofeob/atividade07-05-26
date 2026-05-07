"""
database/db.py
Configuração da conexão com SQLite e criação das tabelas.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "cinema.db")


def get_connection() -> sqlite3.Connection:
    """Retorna uma conexão configurada com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    conn.execute("PRAGMA foreign_keys = ON")  # habilita chaves estrangeiras
    return conn


def inicializar_banco() -> None:
    """Cria todas as tabelas caso ainda não existam."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS cinemas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT    NOT NULL,
            cidade      TEXT    NOT NULL,
            estado      TEXT    NOT NULL,
            endereco    TEXT    NOT NULL,
            capacidade  INTEGER NOT NULL CHECK(capacidade > 0)
        );

        CREATE TABLE IF NOT EXISTS filmes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo       TEXT    NOT NULL,
            duracao_min  INTEGER NOT NULL CHECK(duracao_min > 0),
            genero       TEXT    NOT NULL,
            diretor      TEXT    NOT NULL,
            elenco       TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sessoes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            cinema_id     INTEGER NOT NULL REFERENCES cinemas(id),
            filme_id      INTEGER NOT NULL REFERENCES filmes(id),
            data_hora     TEXT    NOT NULL,
            sala          TEXT    NOT NULL,
            intervalo_min INTEGER NOT NULL DEFAULT 15
        );

        CREATE TABLE IF NOT EXISTS registros_publico (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            sessao_id         INTEGER NOT NULL REFERENCES sessoes(id),
            data              TEXT    NOT NULL,
            quantidade_publico INTEGER NOT NULL CHECK(quantidade_publico >= 0)
        );
    """)

    conn.commit()
    conn.close()
    print("[DB] Banco de dados inicializado com sucesso.")
