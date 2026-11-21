#Classe Lógica para as Validações

class User():
    def validar_credenciais(self, usuario_digitado: str, senha_digitado: str):
        """Função para validação de credenciais"""

        if not usuario_digitado or not senha_digitado:
            return False, f"Erro: Por favor, preencha todos os campos!"

        if usuario_digitado == 'admin' and senha_digitado == '1234':
            return True, f"Sucesso: Bem-vindo, {usuario_digitado}!"
        
        return False, "Erro: Nome de usuário ou senha incorretos."
