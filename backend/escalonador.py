import random
from algoritmos.round_robin import round_robin
from algoritmos.fifo import fifo
from algoritmos.rr_prioridade import round_robin_prioridade


class Escalonador:
    def __init__(self, tipo="RR"):
        self.tipo = tipo              # "RR", "FIFO", "RR_PRI"
        self.processos = []           # Lista de processos
        self.processo_id = 1          # Contador para gerar PID
        self.quantum_fixo = None      # Quantum global (se aplicável)

    def adicionar_processo(self, tempo_exec, quantum_input=None, prioridade_input=None):
        """Adiciona um novo processo com tempo de execução (e prioridade se necessário)"""
        if tempo_exec <= 0:
            return None

        # Define o quantum apenas uma vez (na inserção do primeiro processo)
        if self.tipo in ["RR", "RR_PRI"] and self.quantum_fixo is None:
            try:
                self.quantum_fixo = int(quantum_input)
            except (ValueError, TypeError):
                return None
            if self.quantum_fixo <= 0:
                self.quantum_fixo = None
                return None

        # Cria cor aleatória
        cor = f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"

        processo = {
            "pid": f"P{self.processo_id}",
            "exec": tempo_exec,
            "cor": cor
        }

        # Quantum (se aplicável)
        if self.tipo in ["RR", "RR_PRI"]:
            processo["quantum"] = self.quantum_fixo

        # Prioridade (se aplicável)
        if self.tipo == "RR_PRI":
            try:
                prioridade = int(prioridade_input)
            except (ValueError, TypeError):
                prioridade = None
            if prioridade is None:
                return None
            processo["prioridade"] = prioridade

        self.processos.append(processo)
        self.processo_id += 1
        return processo

    def executar(self):
        """Executa o algoritmo escolhido"""
        if self.tipo == "RR":
            return round_robin(self.processos, self.quantum_fixo)
        elif self.tipo == "FIFO":
            resultados = fifo(self.processos)
            return [r["fim"] for r in resultados]
        elif self.tipo == "RR_PRI":
            return round_robin_prioridade(self.processos, self.quantum_fixo)
        return []

    def resetar(self):
        """Reseta o escalonador"""
        self.processos = []
        self.processo_id = 1
        self.quantum_fixo = None
