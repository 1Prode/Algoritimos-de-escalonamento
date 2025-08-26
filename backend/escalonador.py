import random
from algoritimos.round_robin import round_robin  # Importa a função de escalonamento

class Escalonador:
    def __init__(self):
        self.processos = []           # Lista de processos
        self.processo_id = 1          # Contador para gerar PID
        self.quantum_fixo = None      # Quantum global (definido no primeiro processo)

    def adicionar_processo(self, tempo_exec, quantum_input=None):
        """Adiciona um novo processo com tempo de execução e quantum fixo"""
        if tempo_exec <= 0:
            return None

        # Define o quantum apenas uma vez (na inserção do primeiro processo)
        if self.quantum_fixo is None:
            try:
                self.quantum_fixo = int(quantum_input)
            except (ValueError, TypeError):
                return None
            if self.quantum_fixo <= 0:
                self.quantum_fixo = None
                return None

        # Cria o processo com uma cor aleatória
        quantum = self.quantum_fixo
        cor = f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"

        processo = {
            "pid": f"P{self.processo_id}",
            "exec": tempo_exec,
            "quantum": quantum,
            "cor": cor
        }
        self.processos.append(processo)
        self.processo_id += 1
        return processo

    def executar_round_robin(self):
        """Executa o algoritmo Round Robin nos processos armazenados"""
        return round_robin(self.processos, self.quantum_fixo)

    def resetar(self):
        """Reseta os dados do escalonador"""
        self.processos = []
        self.processo_id = 1
        self.quantum_fixo = None
