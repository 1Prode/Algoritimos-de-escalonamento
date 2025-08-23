import random

class Escalonador:
    def __init__(self):
        self.processos = []
        self.processo_id = 1
        self.quantum_fixo = None

    def adicionar_processo(self, tempo_exec, quantum_input=None):
        if self.quantum_fixo is None:
            try:
                self.quantum_fixo = int(quantum_input)
            except (ValueError, TypeError):
                self.quantum_fixo = 0

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

    # ---------- Algoritmos ----------
    def round_robin(self):
        """Escalonamento Round Robin"""
        if not self.processos or self.quantum_fixo is None or self.quantum_fixo <= 0:
            return []

        tempos = [p["exec"] for p in self.processos]
        n = len(tempos)

        tempo_restante = tempos[:]
        tempo_atual = 0
        tempo_ciclo = [0] * n
        fila = list(range(n))

        while fila:
            i = fila.pop(0)
            if tempo_restante[i] > self.quantum_fixo:
                tempo_atual += self.quantum_fixo
                tempo_restante[i] -= self.quantum_fixo
                fila.append(i)
            else:
                tempo_atual += tempo_restante[i]
                tempo_restante[i] = 0
                tempo_ciclo[i] = tempo_atual

        return tempo_ciclo
    
    def priodirade(self):
        pass

    def resetar(self):
        self.processos = []
        self.processo_id = 1
        self.quantum_fixo = None
