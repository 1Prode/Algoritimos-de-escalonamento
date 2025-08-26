# Simulador de Escalonamento Round Robin

Este projeto implementa um **simulador de escalonamento de processos** usando o algoritmo **Round Robin**, com interface gráfica construída em **CustomTkinter**.

## Funcionalidades
- Adição de processos com:
  - Tempo de execução
  - Quantum (definido apenas no primeiro processo, usado globalmente)
- Execução do algoritmo **Round Robin** para calcular o tempo de finalização de cada processo.
- Interface gráfica que exibe os processos adicionados, cada um com uma cor distinta.
- Reset do simulador para iniciar novos testes.

## Estrutura do Projeto

├── Main.py # Interface gráfica (CustomTkinter)
├── Backend/
│ └── Escalonador.py # Classe que gerencia os processos e conecta ao algoritmo
├── Algoritimos/
│ └── Round_robin.py # Implementação do algoritmo Round Robin


## Como Executar
1. Instale as dependências:
   ```bash
   pip install customtkinter CTkMessagebox

    Execute o programa:

    python main.py

Uso

    Insira o Tempo de Execução do processo.

    Insira o Quantum (este valor é usado como quantum global — depois de adicionar o primeiro processo, o campo de quantum é desabilitado).

    Clique em Adicionar Processo para inserir mais processos.

    Clique em Iniciar Simulação para executar o Round Robin e ver o tempo de finalização de cada processo.

    Use o botão ↻ para resetar o simulador e começar de novo.

Arquivos principais

    main.py — controla a interface gráfica, captura entradas do usuário e mostra resultados.

    backend/escalonador.py — gerencia a lista de processos, gera PIDs, define o quantum global e integra com o algoritmo.

    backend/algoritimos/round_robin.py — simula o algoritmo Round Robin e retorna os tempos de finalização.

Observações sobre o comportamento atual

    O quantum é definido na inserção do primeiro processo e aplicado globalmente a todos os processos subsequentes.

    Cada processo recebe uma cor aleatória para identificação visual no display.

    O simulador retorna os tempos de finalização (tempo em unidades de clock) de cada processo após a execução.

Melhorias Futuras

    Gráfico de Gantt: adicionar uma visualização de Gantt para mostrar a linha do tempo de execução dos processos (eixo X = tempo, eixo Y = processos). O gráfico exibirá as fatias de tempo (quantums) atribuídas a cada processo, permitindo visualizar a alternância de CPU característica do Round Robin.

    Cálculo e exibição de métricas como turnaround time, waiting time e throughput.

    Exportar resultados para CSV ou imagem (ex.: salvar o Gantt como PNG).

    Melhorar a UI para permitir editar/remover processos e ajustar quantum dinamicamente.

    Implementar testes automatizados para validar o algoritmo com diferentes cenários.