def round_robin(processos, quantum):
    # n = quantidade de processos
    n = len(processos)

    # tempo_restante = copia dos tempos de execucao originais
    # (assim podemos descontar o tempo que cada processo ainda precisa rodar
    # sem alterar a lista original)
    tempo_restante = processos[:]

    # tempo_atual = relogio global, comeca em 0
    tempo_atual = 0

    # tempo_ciclo = lista para armazenar o tempo de ciclo de vida de cada processo
    # inicialmente todos com 0
    tempo_ciclo = [0] * n

    # fila = indices dos processos em ordem de chegada (todos chegam no tempo 0)
    # ex: se ha 3 processos → [0, 1, 2]
    fila = list(range(n))

    # Enquanto ainda houver processos na fila
    while fila:
        # retira o primeiro processo da fila
        i = fila.pop(0)

        # Se o tempo restante do processo for maior que o quantum
        if tempo_restante[i] > quantum:
            # o processo executa apenas o quantum
            tempo_atual += quantum
            # desconta o quantum do tempo restante dele
            tempo_restante[i] -= quantum
            # como nao terminou, volta para o final da fila
            fila.append(i)

        else:
            # caso contrario, o processo vai terminar nesta rodada
            tempo_atual += tempo_restante[i]  # soma o que faltava ao relogio
            tempo_restante[i] = 0             # zera o tempo restante
            tempo_ciclo[i] = tempo_atual      # registra o tempo em que terminou

    # retorna a lista com o tempo de ciclo de cada processo
    return tempo_ciclo


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    # Le a quantidade de processos
    n = int(input("Insira a quantidade de processos: "))

    # Le os tempos de execucao de cada processo e guarda em uma lista
    processos = []
    for i in range(n):
        t = int(input(f"Insira o tempo de execucao do processo P{i+1}: "))
        processos.append(t)

    # Le o valor do quantum
    quantum = int(input("Insira o valor do quantum: "))

    # Chama a funcao que simula o Round Robin
    resultado = round_robin(processos, quantum)

    # Exibe o resultado para cada processo
    print("\nTempo do ciclo de vida de cada Processo:")
    for i, tempo in enumerate(resultado):
        print(f"P{i+1}: {tempo} unidades de tempo")
