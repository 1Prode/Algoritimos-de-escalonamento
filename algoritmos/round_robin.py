def round_robin(processos, quantum):
    """Simula o algoritmo de escalonamento Round Robin"""
    if not processos or quantum is None or quantum <= 0:
        return []

    # Lista com os tempos de execução originais
    tempos = [p["exec"] for p in processos]
    n = len(tempos)

    tempo_restante = tempos[:]         # Cópia dos tempos (para reduzir durante execução)
    tempo_atual = 0                    # Tempo global da simulação
    tempo_ciclo = [0] * n              # Tempo de término de cada processo
    fila = list(range(n))              # Fila de índices dos processos

    # Enquanto houver processos na fila
    while fila:
        i = fila.pop(0)  # Pega o próximo processo da fila

        if tempo_restante[i] > quantum:
            # Executa o quantum e volta para o final da fila
            tempo_atual += quantum
            tempo_restante[i] -= quantum
            fila.append(i)
        else:
            # Processo finaliza
            tempo_atual += tempo_restante[i]
            tempo_restante[i] = 0
            tempo_ciclo[i] = tempo_atual

    return tempo_ciclo  # Retorna lista com tempos de finalização
