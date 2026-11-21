import json
import os
from datetime import datetime

class User:
    def __init__(self, arquivo_json="usuarios.json"):
        self.arquivo_json = arquivo_json
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        """Cria o arquivo JSON com um admin padrão caso não exista."""
        if not os.path.exists(self.arquivo_json):
            dados_iniciais = [
                {
                    "nome": "admin",
                    "senha": "1234",
                    "cargo": "Admin",
                    "data_cadastro": datetime.now().strftime("%d/%m/%Y")
                }
            ]
            self._salvar_todos(dados_iniciais)

    def carregar_usuarios(self) -> list:
        with open(self.arquivo_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar_todos(self, lista_usuarios: list):
        with open(self.arquivo_json, "w", encoding="utf-8") as f:
            json.dump(lista_usuarios, f, indent=4, ensure_ascii=False)

    def validar_credenciais(self, usuario_digitado: str, senha_digitado: str):
        if not usuario_digitado or not senha_digitado:
            return False, "Erro: Por favor, preencha todos os campos!", None

        usuarios = self.carregar_usuarios()
        for u in usuarios:
            if u.get("nome").lower() == usuario_digitado.lower() and u.get("senha") == senha_digitado:
                return True, f"Sucesso: Bem-vindo(a), {u['nome']}!", u

        return False, "Erro: Nome de usuário ou senha incorretos.", None

    def cadastrar_usuario(self, nome: str, senha: str, cargo: str):
        if not nome or not senha:
            return False, "Preencha Nome e Senha."

        usuarios = self.carregar_usuarios()
        if any(u["nome"].lower() == nome.lower() for u in usuarios):
            return False, "Já existe um usuário com este nome."

        novo_usuario = {
            "nome": nome,
            "senha": senha,
            "cargo": cargo,
            "data_cadastro": datetime.now().strftime("%d/%m/%Y")
        }
        usuarios.append(novo_usuario)
        self._salvar_todos(usuarios)
        return True, "Usuário cadastrado com sucesso!"

    def excluir_usuario(self, nome: str):
        usuarios = self.carregar_usuarios()
        usuarios_filtrados = [u for u in usuarios if u["nome"].lower() != nome.lower()]
        self._salvar_todos(usuarios_filtrados)