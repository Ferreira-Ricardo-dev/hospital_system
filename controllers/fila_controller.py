import heapq
from datetime import datetime

class GerenciadorFila:
    PRIORIDADES = {
        "Emergência": (1, "EMG"),
        "Preferencial (Idade / Gestante / PCD)": (2, "PRF"),
        "Normal": (3, "NRM")
    }

    def __init__(self):
        self.filas = {
            "Clínico Geral": [],
            "Ortopedista": [],
            "Oftalmologista": []
        }
        self.contador_chegada = 0
        self.contadores_senha = {"EMG": 0, "PRF": 0, "NRM": 0}
        self.ultimo_chamado = None
        self.historico_chamadas = []

    def adicionar_paciente(self, nome: str, idade: int, nivel_prioridade: str, especialidade: str):
        if not nome.strip():
            return False, "Informe o nome do paciente.", None

        peso, prefixo = self.PRIORIDADES[nivel_prioridade]
        self.contador_chegada += 1
        self.contadores_senha[prefixo] += 1

        senha = f"{prefixo}-{self.contadores_senha[prefixo]:03d}"

        paciente = {
            "senha": senha,
            "nome": nome.strip(),
            "idade": idade,
            "prioridade_label": nivel_prioridade,
            "peso": peso,
            "especialidade": especialidade,
            "hora_chegada": datetime.now().strftime("%H:%M:%S")
        }

        heapq.heappush(self.filas[especialidade], (peso, self.contador_chegada, paciente))
        return True, f"Senha {senha} gerada para {paciente['nome']}.", paciente

    def chamar_proximo(self, especialidade: str, consultorio: str = "Consultório 01"):
        fila_alvo = self.filas.get(especialidade, [])
        if not fila_alvo:
            return None

        _, _, paciente = heapq.heappop(fila_alvo)
        paciente["consultorio"] = consultorio
        paciente["hora_chamada"] = datetime.now().strftime("%H:%M:%S")

        self.ultimo_chamado = paciente
        self.historico_chamadas.insert(0, paciente)
        self.historico_chamadas = self.historico_chamadas[:5]

        return paciente

    def listar_fila_ordenada(self, especialidade: str) -> list:
        """Retorna uma cópia ordenada da heap sem remover os elementos (para exibição na UI)."""
        fila_alvo = self.filas.get(especialidade, [])
        return [item[2] for item in sorted(fila_alvo)]