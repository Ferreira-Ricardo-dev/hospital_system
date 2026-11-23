import heapq
import sqlite3
from datetime import datetime
from database import CAMINHO_BANCO, inicializar_banco

class GerenciadorFila:
    PRIORIDADES = {
        "Emergência": (1, "EMG"),
        "Preferencial (Idade / Gestante / PCD)": (2, "PRF"),
        "Normal": (3, "NRM")
    }

    def __init__(self):
        inicializar_banco()
        self.filas = {
            "Clínico Geral": [],
            "Ortopedista": [],
            "Oftalmologista": []
        }
        self.contador_chegada = 0
        self.contadores_senha = {"EMG": 0, "PRF": 0, "NRM": 0}
        self.ultimo_chamado = None
        self.historico_chamadas = []
        conexao = sqlite3.connect(CAMINHO_BANCO)
        try:
            for prefixo, numero in conexao.execute("SELECT prefixo, ultimo_numero FROM contadores_senha"):
                self.contadores_senha[prefixo] = numero
            for id_fila, senha, nome, idade, especialidade, prioridade, peso, data_chegada in conexao.execute(
                "SELECT id, senha, nome, idade, especialidade, prioridade, peso, data_chegada FROM fila_espera ORDER BY id"
            ):
                paciente = {"senha": senha, "nome": nome, "idade": idade,
                    "prioridade_label": prioridade, "peso": peso, "especialidade": especialidade,
                    "hora_chegada": datetime.fromisoformat(data_chegada).strftime("%H:%M:%S")}
                heapq.heappush(self.filas[especialidade], (peso, id_fila, paciente))
                self.contador_chegada = max(self.contador_chegada, id_fila)
            ultima = conexao.execute("""SELECT senha, nome, especialidade, prioridade, consultorio, data_chamada
                FROM ultima_chamada WHERE id = 1""").fetchone()
            if ultima:
                senha, nome, especialidade, prioridade, consultorio, data_chamada = ultima
                self.ultimo_chamado = {"senha": senha, "nome": nome, "especialidade": especialidade,
                    "prioridade_label": prioridade, "consultorio": consultorio,
                    "hora_chamada": datetime.fromisoformat(data_chamada).strftime("%H:%M:%S")}
                self.historico_chamadas = [self.ultimo_chamado]
        finally:
            conexao.close()

    def adicionar_paciente(self, nome: str, idade: int, nivel_prioridade: str, especialidade: str):
        if not nome.strip():
            return False, "Informe o nome do paciente.", None

        peso, prefixo = self.PRIORIDADES[nivel_prioridade]
        numero = self.contadores_senha[prefixo] + 1
        senha = f"{prefixo}-{numero:03d}"
        chegada = datetime.now()

        paciente = {
            "senha": senha,
            "nome": nome.strip(),
            "idade": idade,
            "prioridade_label": nivel_prioridade,
            "peso": peso,
            "especialidade": especialidade,
            "hora_chegada": chegada.strftime("%H:%M:%S")
        }
        conexao = sqlite3.connect(CAMINHO_BANCO)
        try:
            with conexao:
                conexao.execute("UPDATE contadores_senha SET ultimo_numero = ? WHERE prefixo = ?", (numero, prefixo))
                cursor = conexao.execute("""INSERT INTO fila_espera
                    (senha, nome, idade, especialidade, prioridade, peso, data_chegada)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (senha, paciente["nome"], idade, especialidade, nivel_prioridade, peso, chegada.isoformat()))
                id_fila = cursor.lastrowid
        finally:
            conexao.close()
        self.contadores_senha[prefixo] = numero
        self.contador_chegada = id_fila
        heapq.heappush(self.filas[especialidade], (peso, id_fila, paciente))
        return True, f"Senha {senha} gerada para {paciente['nome']}.", paciente

    def chamar_proximo(self, especialidade: str, consultorio: str = "Consultório 01"):
        fila_alvo = self.filas.get(especialidade, [])
        if not fila_alvo:
            return None

        _, id_fila, paciente = fila_alvo[0]
        chamada = datetime.now()
        conexao = sqlite3.connect(CAMINHO_BANCO)
        try:
            with conexao:
                conexao.execute("DELETE FROM fila_espera WHERE id = ?", (id_fila,))
                conexao.execute("""INSERT OR REPLACE INTO ultima_chamada
                    (id, senha, nome, especialidade, prioridade, consultorio, data_chamada)
                    VALUES (1, ?, ?, ?, ?, ?, ?)""",
                    (paciente["senha"], paciente["nome"], paciente["especialidade"],
                     paciente["prioridade_label"], consultorio, chamada.isoformat()))
        finally:
            conexao.close()
        heapq.heappop(fila_alvo)
        paciente["consultorio"] = consultorio
        paciente["hora_chamada"] = chamada.strftime("%H:%M:%S")

        self.ultimo_chamado = paciente
        self.historico_chamadas.insert(0, paciente)
        self.historico_chamadas = self.historico_chamadas[:5]

        return paciente

    def listar_fila_ordenada(self, especialidade: str) -> list:
        """Retorna uma cópia ordenada da heap sem remover os elementos (para exibição na UI)."""
        fila_alvo = self.filas.get(especialidade, [])
        return [item[2] for item in sorted(fila_alvo)]
