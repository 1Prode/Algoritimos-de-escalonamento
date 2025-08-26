import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from backend.escalonador import Escalonador  # Importa o backend de escalonamento

# Classe principal da interface gráfica
class Principal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Escalonamento")

        # Define tamanho fixo da janela e centraliza na tela
        largura, altura = 675, 370
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        self.resizable(False, False)  # Impede redimensionamento

        # Cria a instância do escalonador (backend)
        self.escalonador = Escalonador()

        # Configura layout da janela principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------------- TOPO: Campos de entrada e botões ----------------
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        control_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Campo para inserir o tempo de execução do processo
        self.execucaoIn = ctk.CTkEntry(control_frame, placeholder_text="Tempo de Execução")
        self.execucaoIn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Campo para inserir o quantum
        self.quantumIn = ctk.CTkEntry(control_frame, placeholder_text="Quantum")
        self.quantumIn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botão para adicionar processo à lista
        self.addProcessoBtn = ctk.CTkButton(
            control_frame, text="Adicionar Processo",
            command=self.add_processo, fg_color="purple", hover_color="#4d004d"
        )
        self.addProcessoBtn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Botão para iniciar a simulação
        self.simularBtn = ctk.CTkButton(
            control_frame, text="Iniciar Simulação",
            command=self.simular, fg_color="purple", hover_color="#4d004d"
        )
        self.simularBtn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Botão para resetar o estado do simulador
        self.resetBtn = ctk.CTkButton(
            control_frame, text="↻", width=27, height=27,
            command=self.resetar, fg_color="purple", hover_color="#D30000", corner_radius=8
        )
        self.resetBtn.grid(row=0, column=4, padx=5, pady=5)

        # ---------------- DISPLAY DE SAÍDA ----------------
        # Área que exibe os processos adicionados e os resultados da simulação
        self.display = ctk.CTkScrollableFrame(
            self, label_text="Processos e Resultados", fg_color="transparent"
        )
        self.display.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.display.grid_columnconfigure(0, weight=1)

    # ---------------- MÉTODOS ----------------

    def add_processo(self):
        """Adiciona um novo processo ao escalonador."""
        try:
            tempo_exec = int(self.execucaoIn.get())  # Tempo de execução inserido
            # Quantum: usa valor do campo se ainda não foi definido
            quantum_val = int(self.quantumIn.get()) if self.escalonador.quantum_fixo is None else self.escalonador.quantum_fixo
        except ValueError:
            CTkMessagebox(title="Erro", message="Tempo de Execução e Quantum \nnão podem ser vazio!", icon="warning")
            return

        # Verifica se os valores são válidos
        if tempo_exec <= 0 or quantum_val <= 0:
            CTkMessagebox(title="Erro", message="Tempo de Execução e Quantum \ndeve ser maior que 0!", icon="warning")
            return

        # Adiciona o processo ao backend
        processo = self.escalonador.adicionar_processo(tempo_exec, quantum_val)
        if processo is None:
            return

        # Após o primeiro processo, desabilita o campo de quantum
        if self.escalonador.quantum_fixo is not None:
            self.quantumIn.configure(state="disabled")

        # Mostra o processo no display
        self._criar_item_display(
            processo,
            f"{processo['pid']} | Exec: {tempo_exec} | Quantum: {processo['quantum']}"
        )
        self.execucaoIn.delete(0, "end")  # Limpa o campo

    def simular(self):
        """Executa o algoritmo Round Robin e exibe os resultados."""
        # Limpa o display
        for widget in self.display.winfo_children():
            widget.destroy()

        # Executa o algoritmo
        resultados = self.escalonador.executar_round_robin()

        # Exibe o tempo de finalização de cada processo
        for i, p in enumerate(self.escalonador.processos):
            texto = f"{p['pid']} finalizou em {resultados[i]} unidades de tempo"
            self._criar_item_display(p, texto)

    def resetar(self):
        """Reseta o escalonador e a interface gráfica."""
        self.escalonador.resetar()
        self.quantumIn.configure(state="normal")
        self.quantumIn.delete(0, "end")
        self.execucaoIn.delete(0, "end")
        for widget in self.display.winfo_children():
            widget.destroy()

    def _criar_item_display(self, processo, texto):
        """Adiciona um item ao display (interface)."""
        item = ctk.CTkFrame(self.display, corner_radius=20)
        item.pack(fill="x", pady=5, padx=5)

        # Círculo com a cor do processo
        bola = ctk.CTkLabel(item, text="●", text_color=processo["cor"], font=("Arial", 28))
        bola.pack(side="left", padx=10, pady=(0, 5))

        # Texto com informações
        info = ctk.CTkLabel(item, text=texto)
        info.pack(side="left", padx=17)


# Executa o app
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Principal()
    app.mainloop()
