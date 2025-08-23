import customtkinter as ctk
from algoritimos.roundrobin import Escalonador

class Principal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Escalonamento")

        largura, altura = 675, 370
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        self.resizable(False, False)

        # Instância do backend
        self.escalonador = Escalonador()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        control_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.execucaoIn = ctk.CTkEntry(control_frame, placeholder_text="Tempo de Execução")
        self.execucaoIn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.quantumIn = ctk.CTkEntry(control_frame, placeholder_text="Quantum")
        self.quantumIn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.addProcessoBtn = ctk.CTkButton(
            control_frame, text="Adicionar Processo",
            command=self.add_processo, fg_color="purple", hover_color="#4d004d"
        )
        self.addProcessoBtn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.simularBtn = ctk.CTkButton(
            control_frame, text="Iniciar Simulação",
            command=self.simular, fg_color="purple", hover_color="#4d004d"
        )
        self.simularBtn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.resetBtn = ctk.CTkButton(
            control_frame, text="↻", width=27, height=27,
            command=self.resetar, fg_color="purple", hover_color="#D30000", corner_radius=8
        )
        self.resetBtn.grid(row=0, column=4, padx=5, pady=5)

        self.display = ctk.CTkScrollableFrame(self, label_text="Processos e Resultados", fg_color="transparent")
        self.display.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.display.grid_columnconfigure(0, weight=1)

    def add_processo(self):
        try:
            tempo_exec = int(self.execucaoIn.get())
        except ValueError:
            tempo_exec = 0

        processo = self.escalonador.adicionar_processo(tempo_exec, self.quantumIn.get())
        if self.escalonador.quantum_fixo is not None:
            self.quantumIn.configure(state="disabled")

        self._criar_item_display(processo, f"{processo['pid']} | Exec: {tempo_exec} | Quantum: {processo['quantum']}")
        self.execucaoIn.delete(0, "end")

    def simular(self):
        for widget in self.display.winfo_children():
            widget.destroy()

        # Aqui você pode trocar o método de escalonamento
        resultados = self.escalonador.round_robin()

        for i, p in enumerate(self.escalonador.processos):
            texto = f"{p['pid']} finalizou em {resultados[i]} unidades de tempo"
            self._criar_item_display(p, texto)

    def resetar(self):
        self.escalonador.resetar()
        self.quantumIn.configure(state="normal")
        self.quantumIn.delete(0, "end")
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


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Principal()
    app.mainloop()
