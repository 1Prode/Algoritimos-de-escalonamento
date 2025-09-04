import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from backend.escalonador import Escalonador


# -------------------- Classe Base para Simuladores --------------------
class SimuladorBase(ctk.CTkToplevel):
    def __init__(self, algoritmo_nome, escalonador_factory, fechar_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurações da janela
        self.title(f"Simulador - {algoritmo_nome}")
        largura, altura = 675, 400
        x = (self.winfo_screenwidth() // 2) - (largura // 2) + 40
        y = (self.winfo_screenheight() // 2) - (altura // 2) + 40
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        self.resizable(False, False)

        # Cria instância do backend específico
        self.escalonador = escalonador_factory()
        self.algoritmo_nome = algoritmo_nome
        self.fechar_callback = fechar_callback
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------------- TOPO ----------------
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        control_frame.grid_columnconfigure(0, weight=2)  # Execução
        control_frame.grid_columnconfigure(1, weight=1)  # Quantum
        control_frame.grid_columnconfigure(2, weight=2)  # Prioridade
        control_frame.grid_columnconfigure(3, weight=3)  # Botão Adicionar
        control_frame.grid_columnconfigure(4, weight=3)  # Botão Simular
        control_frame.grid_columnconfigure(5, weight=1)  # Botão Reset

        # Entradas
        self.execucaoIn = ctk.CTkEntry(control_frame, placeholder_text="Tempo de Execução")
        self.execucaoIn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.quantumIn = None
        if algoritmo_nome in ["Round Robin", "Round Robin com Prioridade"]:
            self.quantumIn = ctk.CTkEntry(control_frame, placeholder_text="Quantum", width=80)
            self.quantumIn.grid(row=0, column=1, padx=3, pady=5)

        self.prioridadeIn = None
        if algoritmo_nome == "Round Robin com Prioridade":
            placeholder_texto = "Prioridade (menor = mais alta)"
            self.prioridadeIn = ctk.CTkEntry(control_frame, placeholder_text=placeholder_texto)
            self.prioridadeIn.grid(row=0, column=2, padx=3, pady=5, sticky="ew")

        # Botões
        self.addProcessoBtn = ctk.CTkButton(
            control_frame, text="Adicionar Processo",
            command=self.add_processo, fg_color="purple", hover_color="#4d004d"
        )
        self.addProcessoBtn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.simularBtn = ctk.CTkButton(
            control_frame, text="Iniciar Simulação",
            command=self.simular, fg_color="purple", hover_color="#4d004d"
        )
        self.simularBtn.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        self.resetBtn = ctk.CTkButton(
            control_frame, text="↻", width=40, height=30,
            command=self.resetar, fg_color="purple", hover_color="#D30000", corner_radius=8
        )
        self.resetBtn.grid(row=0, column=5, padx=5, pady=5)

        # ---------------- DISPLAY ----------------
        self.display = ctk.CTkScrollableFrame(
            self, label_text="Processos e Resultados", fg_color="transparent"
        )
        self.display.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.display.grid_columnconfigure(0, weight=1)

    def _on_close(self):
        self.fechar_callback(self.algoritmo_nome)
        self.destroy()

    # ---------------- MÉTODOS ----------------
    def add_processo(self):
        try:
            tempo_exec = int(self.execucaoIn.get())
            quantum_val = None
            prioridade_val = None

            if self.quantumIn is not None:
                quantum_val = int(self.quantumIn.get()) if self.escalonador.quantum_fixo is None else self.escalonador.quantum_fixo

            if self.prioridadeIn is not None and self.prioridadeIn.get().strip():
                prioridade_val = int(self.prioridadeIn.get())

        except ValueError:
            CTkMessagebox(title="Erro", message="Preencha os campos corretamente!", icon="warning")
            return

        if tempo_exec <= 0 or (quantum_val is not None and quantum_val <= 0):
            CTkMessagebox(title="Erro", message="Valores devem ser maiores que 0!", icon="warning")
            return

        processo = self.escalonador.adicionar_processo(tempo_exec, quantum_val, prioridade_val)
        if processo is None:
            return

        if self.escalonador.quantum_fixo is not None and self.quantumIn is not None:
            self.quantumIn.configure(state="disabled")

        texto = f"{processo['pid']} | Exec: {tempo_exec}"
        if "quantum" in processo:
            texto += f" | Quantum: {processo.get('quantum')}"
        if "prioridade" in processo:
            texto += f" | Prioridade: {processo['prioridade']}"

        self._criar_item_display(processo, texto)
        self.execucaoIn.delete(0, "end")
        if self.prioridadeIn is not None:
            self.prioridadeIn.delete(0, "end")

    def simular(self):
        for widget in self.display.winfo_children():
            widget.destroy()

        resultados = self.escalonador.executar()
        for i, p in enumerate(self.escalonador.processos):
            texto = f"{p['pid']} finalizou em {resultados[i]} unidades de tempo"
            self._criar_item_display(p, texto)

    def resetar(self):
        self.escalonador.resetar()
        if self.quantumIn is not None:
            self.quantumIn.configure(state="normal")
            self.quantumIn.delete(0, "end")
        if self.prioridadeIn is not None:
            self.prioridadeIn.delete(0, "end")
        self.execucaoIn.delete(0, "end")
        for widget in self.display.winfo_children():
            widget.destroy()

    def _criar_item_display(self, processo, texto):
        item = ctk.CTkFrame(self.display, corner_radius=20)
        item.pack(fill="x", pady=5, padx=5)

        bola = ctk.CTkLabel(item, text="●", text_color=processo["cor"], font=("Arial", 28))
        bola.pack(side="left", padx=10, pady=(0, 5))

        info = ctk.CTkLabel(item, text=texto)
        info.pack(side="left", padx=17)


# -------------------- Menu Inicial --------------------
class MenuInicial(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menu - Simulador de Escalonamento")
        self.geometry("450x350")
        self.resizable(False, False)
        self.janelas_abertas = {}

        ctk.CTkLabel(self, text="Escolha o Algoritmo", font=("Arial", 18, "bold")).pack(pady=20)
        ctk.CTkButton(self, text="Round Robin", command=self.abrir_round_robin).pack(pady=10)
        ctk.CTkButton(self, text="FIFO", command=self.abrir_FIFO).pack(pady=10)
        ctk.CTkButton(self, text="Round Robin \ncom Prioridade", command=self.abrir_rrPrioridade).pack(pady=10)

    def abrir_janela(self, nome, factory):
        if nome in self.janelas_abertas:
            self.janelas_abertas[nome].focus()
            return
        janela = SimuladorBase(nome, factory, self.fechar_janela)
        self.janelas_abertas[nome] = janela

    def fechar_janela(self, nome):
        if nome in self.janelas_abertas:
            del self.janelas_abertas[nome]

    def abrir_round_robin(self):
        self.abrir_janela("Round Robin", lambda: Escalonador("RR"))

    def abrir_FIFO(self):
        self.abrir_janela("FIFO", lambda: Escalonador("FIFO"))

    def abrir_rrPrioridade(self):
        self.abrir_janela("Round Robin com Prioridade", lambda: Escalonador("RR_PRI"))


# -------------------- MAIN --------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MenuInicial()
    app.mainloop()
