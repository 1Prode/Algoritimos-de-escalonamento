def round_robin_prioridades():
    # Entradas
    n = int(input("Digite o número de processos: ")) #solicita o número de processos
    quantum = int(input("Digite o valor do quantum: ")) #solicita o valor do quantum

    processos = [] #lista para armazenar os nomes dos processos
    burst_time = []    #lista para armazenar os tempos de execução (burst time)
    prioridades = []    #lista para armazenar as prioridades dos processos
    restante = []   #lista para armazenar o tempo restante de cada processo
    tempo_execucao = {} #dicionário para armazenar o tempo de execução de cada processo

    for i in range(n): #loop para coletar informações de cada processo
        processos.append("P" + str(i+1))    #adiciona o nome do processo à lista
        burst_time_value = int(input(f"Digite o tempo de execução (burst time) do processo {processos[i]}: "))    #solicita o tempo de execução do processo em questão
        priority = int(input(f"Digite a prioridade do processo {processos[i]} (quanto menor, maior a prioridade): "))    #solicita a prioridade do processo em questão
        burst_time.append(burst_time_value)  #adiciona o tempo de execução à lista
        prioridades.append(priority)    #adiciona a prioridade à lista
        restante.append(burst_time_value)   #adiciona o tempo restante (inicialmente igual ao burst time) à lista
        tempo_execucao[processos[i]] = 0    #inicializa o tempo de execução do processo como 0

    tempo_total = 0  # Tempo total decorrido
    fila = list(range(n))  # Índices dos processos
    print("\n--- Execução do Round Robin com Prioridades ---")

    # Enquanto houver processos restantes
    while any(r > 0 for r in restante):
        # Ordena a fila pela prioridade (menor valor = maior prioridade)
        fila.sort(key=lambda i: prioridades[i])

        for i in fila:  #para cada processo na fila ordenada por prioridade
            if restante[i] > 0: #se o processo ainda tiver tempo restante
                # Executa o processo pelo quantum ou até terminar
                exec_time = min(quantum, restante[i])   #determina o tempo de execução como o mínimo entre o quantum e o tempo restante
                restante[i] -= exec_time    #diminui o tempo restante pelo tempo de execução
                tempo_total += exec_time    #incrementa o tempo total decorrido
                tempo_execucao[processos[i]] = tempo_total  #atualiza o tempo de execução do processo
                print(f"{processos[i]} executou por {exec_time} unidades de tempo (restante: {restante[i]})")   #exibe o status do processo após a execução

    # Exibe resultados
    print("\n--- Resultado Final ---")
    print("Processo | Burst Time | Prioridade | Tempo de Conclusão")
    for i in range(n):  #para cada processo
        print(f"{processos[i]:8} | {burst_time[i]:10} | {prioridades[i]:10} | {tempo_execucao[processos[i]]:17}")   #exibe os detalhes do processo


# Executar
round_robin_prioridades()
