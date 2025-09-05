def sjf(processos):
    tempo = 0
    resultado = []

    # ordena os processos pelo tempo de execução (exec)
    ordenados = sorted(processos, key=lambda p: p['exec'])

    for p in ordenados:
        inicio = tempo
        fim = inicio + p['exec']
        resultado.append({'pid': p['pid'], 'inicio': inicio, 'fim': fim})
        tempo = fim

    return resultado