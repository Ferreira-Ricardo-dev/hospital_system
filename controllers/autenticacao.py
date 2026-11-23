import sqlite3
from datetime import datetime
from database import CAMINHO_BANCO, inicializar_banco

class User:
    def __init__(self, arquivo_json="usuarios.json"):
        self.arquivo_json = arquivo_json
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        inicializar_banco()

    def carregar_usuarios(self) -> list:
        conexao = sqlite3.connect(CAMINHO_BANCO)
        try:
            linhas = conexao.execute("SELECT nome, senha, cargo, data_cadastro FROM usuarios ORDER BY id").fetchall()
            return [dict(zip(("nome", "senha", "cargo", "data_cadastro"), linha)) for linha in linhas]
        finally:
            conexao.close()

    def validar_credenciais(self, usuario_digitado: str, senha_digitado: str):
        if not usuario_digitado or not senha_digitado:
            return False, "Erro: Por favor, preencha todos os campos!", None

        for u in self.carregar_usuarios():
            if u.get("nome").lower() == usuario_digitado.lower() and u.get("senha") == senha_digitado:
                return True, f"Sucesso: Bem-vindo(a), {u['nome']}!", u

        return False, "Erro: Nome de usuário ou senha incorretos.", None

    def cadastrar_usuario(self, nome: str, senha: str, cargo: str):
        if not nome or not senha:
            return False, "Preencha Nome e Senha."

        if any(u["nome"].lower() == nome.lower() for u in self.carregar_usuarios()):
            return False, "Já existe um usuário com este nome."
        conexao = sqlite3.connect(CAMINHO_BANCO)
        try:
            with conexao:
                conexao.execute("""INSERT INTO usuarios (nome, senha, cargo, data_cadastro)
                    VALUES (?, ?, ?, ?)""", (nome, senha, cargo, datetime.now().strftime("%d/%m/%Y")))
        except sqlite3.IntegrityError:
            return False, "Já existe um usuário com este nome."
        finally:
            conexao.close()
        return True, "Usuário cadastrado com sucesso!"

    def excluir_usuario(self, nome: str):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        try:
            with conexao:
                conexao.execute("DELETE FROM usuarios WHERE nome = ? COLLATE NOCASE", (nome,))
        finally:
            conexao.close()
