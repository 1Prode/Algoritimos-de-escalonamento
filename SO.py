def round_robin (processos, quantum):
    n = len(processos)
    tempo_restante = processos[:]
    ciclo_atual = 0
    ciclo_atual = [0] * n 
    print(ciclo_atual)
    fila = list(range(n))

    while fila:
        i = fila.pop(0)


    return




if __name__ == "__main__":
    processos_IN = int(input("Insira a quantidade de processos: "))
    processos = []
    for i in range(processos_IN):
        tempo = int(input(f"Insira o tempo de execucao do processo P{i+1}: "))
        processos.append(processos_IN)

    quantum = int(input("Insira o valor do quantum: "))

    # Execucao do Round Robin
    resultado = round_robin(processos, quantum)

    # Saida
    print("\nTempo do ciclo de vida de cada Processo:")
    for i, tempo in enumerate(resultado):
        print(f"P{i+1}: {tempo} unidades de tempo")
