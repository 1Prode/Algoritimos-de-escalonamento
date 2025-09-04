def round_robin_prioridade(processos, quantum):
    if not processos or quantum is None or quantum <= 0:
        return []

    n = len(processos)
    restante = [p["exec"] for p in processos]
    prioridades = [p["prioridade"] for p in processos]
    tempo_ciclo = [0] * n
    tempo_atual = 0

    fila = list(range(n))

    while any(r > 0 for r in restante):
        fila.sort(key=lambda i: prioridades[i])  # menor valor = maior prioridade
        for i in fila:
            if restante[i] > 0:
                exec_time = min(quantum, restante[i])
                restante[i] -= exec_time
                tempo_atual += exec_time
                if restante[i] == 0:
                    tempo_ciclo[i] = tempo_atual

    return tempo_ciclo
