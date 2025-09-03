def fifo(processos):
    
    tempo = 0            # marca o tempo atual da CPU
    resultado = []       # guarda os intervalos de execução

    # percorre os processos na ordem que foram adicionados
    for p in processos:
        inicio = tempo           # processo começa quando a CPU está livre
        fim = inicio + p['exec'] # processo termina após seu tempo de execução

        # guarda no resultado o período ocupado pelo processo
        resultado.append({
            'pid': p['pid'],
            'inicio': inicio,
            'fim': fim
        })

        tempo = fim  # atualiza o tempo para o próximo processo

    return resultado