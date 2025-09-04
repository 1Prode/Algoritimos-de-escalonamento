import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from backend.escalonador import Escalonador


# -------------------- FIFO --------------------
class SimuladorFIFO(ctk.CTkToplevel):
    def __init__(self, fechar_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Simulador - FIFO")
        self.geometry("470x400")
        self.resizable(False, False)

        self.escalonador = Escalonador("FIFO")
        self.fechar_callback = fechar_callback
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # --- Inputs e Botões lado a lado ---
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=5)

        self.execucaoIn = ctk.CTkEntry(top_frame, placeholder_text="Tempo de Execução", width=150, corner_radius=15)
        self.execucaoIn.pack(side="left", padx=15)

        ctk.CTkButton(top_frame, text="Adicionar", command=self.add_processo, width=130, fg_color="green", hover_color="green", corner_radius=15).pack(side="left", padx=20)
        ctk.CTkButton(top_frame, text="Simular", command=self.simular, width=130, fg_color="green", hover_color="green", corner_radius=15).pack(side="left", padx=15)
        ctk.CTkButton(top_frame, text="↻", command=self.resetar, width=30, fg_color="green", hover_color="green", corner_radius=15).pack(side="right", padx=13)

        # Display
        self.display = ctk.CTkScrollableFrame(self, label_text="Processos e Resultados")
        self.display.pack(expand=True, fill="both", padx=10, pady=3)

    def _on_close(self):
        self.fechar_callback("FIFO")
        self.destroy()

    def add_processo(self):
        try:
            tempo_exec = int(self.execucaoIn.get())
            if tempo_exec <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(title="Erro", message="Digite um tempo válido!", icon="warning")
            return

        processo = self.escalonador.adicionar_processo(tempo_exec)
        texto = f"{processo['pid']} | Exec: {tempo_exec}"
        self._criar_item_display(processo, texto)
        self.execucaoIn.delete(0, "end")

    def simular(self):
        for w in self.display.winfo_children():
            w.destroy()
        resultados = self.escalonador.executar()
        for i, p in enumerate(self.escalonador.processos):
            texto = f"{p['pid']} finalizou em {resultados[i]} unidades de tempo"
            self._criar_item_display(p, texto)

    def resetar(self):
        self.escalonador.resetar()
        self.execucaoIn.delete(0, "end")
        for w in self.display.winfo_children():
            w.destroy()

    def _criar_item_display(self, processo, texto):
        item = ctk.CTkFrame(self.display, corner_radius=15)
        item.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(item, text="●", text_color=processo["cor"], font=("Arial", 25)).pack(side="left",padx=20)
        ctk.CTkLabel(item, text=texto).pack(side="left", padx=10)


# -------------------- Round Robin --------------------
class SimuladorRR(ctk.CTkToplevel):
    def __init__(self, fechar_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Simulador - Round Robin")
        self.geometry("650x400")
        self.resizable(False, False)

        self.escalonador = Escalonador("RR")
        self.fechar_callback = fechar_callback
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # --- Inputs e Botões lado a lado ---
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=10)

        self.execucaoIn = ctk.CTkEntry(top_frame, placeholder_text="Tempo Execução", width=150, corner_radius=15)
        self.execucaoIn.pack(side="left", padx=8)

        self.quantumIn = ctk.CTkEntry(top_frame, placeholder_text="Quantum", width=100, corner_radius=15)
        self.quantumIn.pack(side="left", padx=8)

        ctk.CTkButton(top_frame, text="Adicionar", command=self.add_processo, width=120, fg_color="purple", hover_color="purple", corner_radius=15).pack(side="left", padx=8)
        ctk.CTkButton(top_frame, text="Simular", command=self.simular, width=120, fg_color="purple", hover_color="purple", corner_radius=15).pack(side="left", padx=8)
        ctk.CTkButton(top_frame, text="↻", command=self.resetar, width=30, fg_color="purple", hover_color="purple", corner_radius=15).pack(side="right", padx=8)

        # Display
        self.display = ctk.CTkScrollableFrame(self, label_text="Processos e Resultados")
        self.display.pack(expand=True, fill="both", padx=10, pady=3)

    def _on_close(self):
        self.fechar_callback("Round Robin")
        self.destroy()

    def add_processo(self):
        try:
            tempo_exec = int(self.execucaoIn.get())
            quantum = int(self.quantumIn.get())
            if tempo_exec <= 0 or quantum <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(title="Erro", message="Preencha corretamente os campos!", icon="warning")
            return

        processo = self.escalonador.adicionar_processo(tempo_exec, quantum)
        texto = f"{processo['pid']} | Exec: {tempo_exec} | Quantum: {quantum}"
        self._criar_item_display(processo, texto)
        self.execucaoIn.delete(0, "end")

    def simular(self):
        for w in self.display.winfo_children():
            w.destroy()
        resultados = self.escalonador.executar()
        for i, p in enumerate(self.escalonador.processos):
            texto = f"{p['pid']} finalizou em {resultados[i]} unidades de tempo"
            self._criar_item_display(p, texto)

    def resetar(self):
        self.escalonador.resetar()
        self.execucaoIn.delete(0, "end")
        self.quantumIn.delete(0, "end")
        for w in self.display.winfo_children():
            w.destroy()

    def _criar_item_display(self, processo, texto):
        item = ctk.CTkFrame(self.display, corner_radius=15)
        item.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(item, text="●", text_color=processo["cor"], font=("Arial", 25)).pack(side="left", padx=10)
        ctk.CTkLabel(item, text=texto).pack(side="left", padx=10)


# -------------------- Round Robin com Prioridade --------------------
class SimuladorRRPrioridade(ctk.CTkToplevel):
    def __init__(self, fechar_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Simulador - RR com Prioridade")
        self.geometry("700x450")
        self.resizable(False, False)

        self.escalonador = Escalonador("RR_PRI")
        self.fechar_callback = fechar_callback
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # --- Inputs e Botões lado a lado ---
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=10)

        self.execucaoIn = ctk.CTkEntry(top_frame, placeholder_text="Execução", width=120, corner_radius=15)
        self.execucaoIn.pack(side="left", padx=8)

        self.quantumIn = ctk.CTkEntry(top_frame, placeholder_text="Quantum", width=90, corner_radius=15)
        self.quantumIn.pack(side="left", padx=8)

        self.prioridadeIn = ctk.CTkEntry(top_frame, placeholder_text="Prioridade", width=120, corner_radius=15)
        self.prioridadeIn.pack(side="left", padx=8)

        ctk.CTkButton(top_frame, text="Adicionar", command=self.add_processo, width=90, fg_color="blue", hover_color="blue", corner_radius=15).pack(side="left", padx=8)
        ctk.CTkButton(top_frame, text="Simular", command=self.simular, width=90, fg_color="blue", hover_color="blue", corner_radius=15).pack(side="left", padx=8)
        ctk.CTkButton(top_frame, text="↻", command=self.resetar, width=70, fg_color="blue", hover_color="blue", corner_radius=15).pack(side="right", padx=8)

        # Display
        self.display = ctk.CTkScrollableFrame(self, label_text="Processos e Resultados")
        self.display.pack(expand=True, fill="both", padx=10, pady=3)

    def _on_close(self):
        self.fechar_callback("Round Robin com Prioridade")
        self.destroy()

    def add_processo(self):
        try:
            tempo_exec = int(self.execucaoIn.get())
            quantum = int(self.quantumIn.get())
            prioridade = int(self.prioridadeIn.get())
            if tempo_exec <= 0 or quantum <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(title="Erro", message="Preencha corretamente os campos!", icon="warning")
            return

        processo = self.escalonador.adicionar_processo(tempo_exec, quantum, prioridade)
        texto = f"{processo['pid']} | Exec: {tempo_exec} | Q: {quantum} | P: {prioridade}"
        self._criar_item_display(processo, texto)
        self.execucaoIn.delete(0, "end")
        self.prioridadeIn.delete(0, "end")

    def simular(self):
        for w in self.display.winfo_children():
            w.destroy()
        resultados = self.escalonador.executar()
        for i, p in enumerate(self.escalonador.processos):
            texto = f"{p['pid']} finalizou em {resultados[i]} unidades de tempo"
            self._criar_item_display(p, texto)

    def resetar(self):
        self.escalonador.resetar()
        self.execucaoIn.delete(0, "end")
        self.quantumIn.delete(0, "end")
        self.prioridadeIn.delete(0, "end")
        for w in self.display.winfo_children():
            w.destroy()

    def _criar_item_display(self, processo, texto):
        item = ctk.CTkFrame(self.display, corner_radius=15)
        item.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(item, text="●", text_color=processo["cor"], font=("Arial", 25)).pack(side="left", padx=10)
        ctk.CTkLabel(item, text=texto).pack(side="left", padx=10)


# -------------------- Menu Inicial --------------------
class MenuInicial(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menu - Simulador de Escalonamento")
        self.geometry("450x300")
        self.resizable(False, False)
        self.janelas_abertas = {}

        ctk.CTkLabel(self, text="Escolha o Algoritmo", font=("Arial", 18, "bold")).pack(pady=20)
        ctk.CTkButton(self, text="FIFO", command=self.abrir_fifo).pack(pady=10)
        ctk.CTkButton(self, text="Round Robin", command=self.abrir_rr).pack(pady=10)
        ctk.CTkButton(self, text="Round Robin com Prioridade", command=self.abrir_rrp).pack(pady=10)

    def abrir_fifo(self):
        if "FIFO" in self.janelas_abertas:
            self.janelas_abertas["FIFO"].focus()
            return
        janela = SimuladorFIFO(self.fechar_janela)
        janela.update_idletasks()

        # Calcula posição dinâmica
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        width = 470  # largura da janela FIFO
        height = 400
        x = int(screen_w * 0.05)  # 5% da tela da esquerda
        y = int((screen_h - height) / 2)  # centralizada verticalmente
        janela.geometry(f"{width}x{height}+{x}+{y}")

        self.janelas_abertas["FIFO"] = janela

    def abrir_rr(self):
        if "Round Robin" in self.janelas_abertas:
            self.janelas_abertas["Round Robin"].focus()
            return
        janela = SimuladorRR(self.fechar_janela)
        janela.update_idletasks()

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        width = 650
        height = 400
        x = int((screen_w - width) / 2)  # centro horizontal
        y = int((screen_h - height) / 2)  # centro vertical
        janela.geometry(f"{width}x{height}+{x}+{y}")

        self.janelas_abertas["Round Robin"] = janela

    def abrir_rrp(self):
        if "Round Robin com Prioridade" in self.janelas_abertas:
            self.janelas_abertas["Round Robin com Prioridade"].focus()
            return
        janela = SimuladorRRPrioridade(self.fechar_janela)
        janela.update_idletasks()

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        width = 700
        height = 450
        x = int(screen_w * 0.85 - width)  # 85% da tela da direita, subtrai largura
        y = int((screen_h - height) / 2)  # centralizada verticalmente
        janela.geometry(f"{width}x{height}+{x}+{y}")

        self.janelas_abertas["Round Robin com Prioridade"] = janela



    def fechar_janela(self, nome):
        if nome in self.janelas_abertas:
            del self.janelas_abertas[nome]


# -------------------- MAIN --------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MenuInicial()
    app.mainloop()
