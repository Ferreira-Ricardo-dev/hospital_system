import json
import sqlite3
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    DIRETORIO_BASE = Path(sys.executable).resolve().parent
else:
    DIRETORIO_BASE = Path(__file__).resolve().parent

CAMINHO_BANCO = DIRETORIO_BASE / "hospital_system.db"
CAMINHO_USUARIOS = DIRETORIO_BASE / "usuarios.json"


def inicializar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    try:
        with conexao:
            conexao.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
                senha TEXT NOT NULL,
                cargo TEXT NOT NULL,
                data_cadastro TEXT NOT NULL
            )""")
            conexao.execute("""CREATE TABLE IF NOT EXISTS fila_espera (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                senha TEXT NOT NULL,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                especialidade TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                peso INTEGER NOT NULL,
                data_chegada TEXT NOT NULL
            )""")
            conexao.execute("""CREATE TABLE IF NOT EXISTS contadores_senha (
                prefixo TEXT PRIMARY KEY,
                ultimo_numero INTEGER NOT NULL
            )""")
            conexao.execute("""CREATE TABLE IF NOT EXISTS ultima_chamada (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                senha TEXT NOT NULL,
                nome TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                consultorio TEXT NOT NULL,
                data_chamada TEXT NOT NULL
            )""")
            for prefixo in ("EMG", "PRF", "NRM"):
                conexao.execute("INSERT OR IGNORE INTO contadores_senha VALUES (?, 0)", (prefixo,))

            if conexao.execute("PRAGMA user_version").fetchone()[0] == 0:
                if CAMINHO_USUARIOS.exists():
                    try:
                        with CAMINHO_USUARIOS.open("r", encoding="utf-8") as arquivo:
                            usuarios = json.load(arquivo)
                        if not isinstance(usuarios, list):
                            raise ValueError("a raiz do JSON deve ser uma lista")
                        for usuario in usuarios:
                            if not isinstance(usuario, dict) or any(campo not in usuario for campo in ("nome", "senha", "cargo", "data_cadastro")):
                                raise ValueError("registro de usuário incompleto")
                            conexao.execute("""INSERT OR IGNORE INTO usuarios
                                (nome, senha, cargo, data_cadastro) VALUES (?, ?, ?, ?)""",
                                (usuario["nome"], usuario["senha"], usuario["cargo"], usuario["data_cadastro"]))
                    except (OSError, ValueError, TypeError, sqlite3.Error) as erro:
                        raise RuntimeError(f"Não foi possível importar usuarios.json: {erro}") from erro
                if not conexao.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone():
                    from datetime import datetime
                    conexao.execute("""INSERT INTO usuarios (nome, senha, cargo, data_cadastro)
                        VALUES (?, ?, ?, ?)""", ("admin", "1234", "Admin", datetime.now().strftime("%d/%m/%Y")))
                conexao.execute("PRAGMA user_version = 1")
    finally:
        conexao.close()
