listaprocessos = []

processo_IN = input("Digite a quantidade de processos que deseja iniciar: ")

for i in range(int(processo_IN)):
    processo_EXE = input(f"Digite o tempo de execução do processo P{i + 1}: ")
    if (processo_EXE.isdigit() and int(processo_EXE) > 0):
        listaprocessos.append(processo_EXE)
    else:
        print("Entrada inválida. Por favor, insira um número inteiro positivo.")

print("Processos em andamento:", listaprocessos)

# if __name__ == "__main__"