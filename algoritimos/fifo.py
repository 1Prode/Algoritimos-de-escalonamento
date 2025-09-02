DEBUG = True  # coloque False ou remova para silenciar prints

def adicionar_processo(fila, pid, tempo_execucao, vezes=1):
    """
    Adiciona um processo à fila 'vezes' vezes.
    Cada entrada é { 'pid': str, 'exec': float }.
    """
    try:
        vezes = int(vezes)
    except:
        vezes = 1
    if vezes < 1:
        vezes = 1

    for _ in range(vezes):
        fila.append({'pid': pid, 'exec': float(tempo_execucao)})

def fifo(processos):
    """
    Executa FIFO (FCFS) na ordem da lista.
    Retorna (resultado, texto):
      - resultado: [{'pid', 'inicio', 'fim'}, ...]
      - texto: string pronta pra exibir no console
    """
    tempo = 0
    resultado = []
    texto = ""

    for p in processos:
        inicio = tempo
        fim = inicio + p['exec']
        resultado.append({'pid': p['pid'], 'inicio': inicio, 'fim': fim})

        if DEBUG:
            print(f"[DEBUG] {p['pid']} | início: {inicio} | fim: {fim}")

        texto += f"Processo {p['pid']} | Início: {inicio} | Fim: {fim}\n"
        tempo = fim

    return resultado, texto


# ===== Bloco de teste (REMOVÍVEL) =====
if __name__ == "__main__":
    fila = []

    # adiciona processos
    adicionar_processo(fila, pid="P1", tempo_execucao=5, vezes=1)  # entra 1 vez
    adicionar_processo(fila, pid="P2", tempo_execucao=3, vezes=2)  # entra 2 vezes
    adicionar_processo(fila, pid="P3", tempo_execucao=2, vezes=1)  # entra 1 vez

    if DEBUG:
        print("[DEBUG] Fila montada:", fila)

    res, saida = fifo(fila)

    print("\n=== Resultado (objeto) ===")
    print(res)

    print("\n=== Resultado (texto) ===")
    print(saida)