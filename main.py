import customtkinter as ctk
import random

class Principal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Escalonamento")
        self.geometry("600x300")

        # Configura o grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---- Frame superior (controles) ----
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        control_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.execucaoIn = ctk.CTkEntry(control_frame, placeholder_text="Tempo de Execução")
        self.execucaoIn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.quantumIn = ctk.CTkEntry(control_frame, placeholder_text="Quantum")
        self.quantumIn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.addProcessoBtn = ctk.CTkButton(control_frame, text="Adicionar Processo", command=self.add_processo, fg_color="purple", hover_color="#4d004d")
        self.addProcessoBtn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.simularBtn = ctk.CTkButton(control_frame, text="Iniciar Simulação", command=self.simular, fg_color="purple", hover_color="#4d004d")
        self.simularBtn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # ---- Área de exibição (processos/resultados) ----
        self.display = ctk.CTkScrollableFrame(self, label_text="Processos e Resultados")
        self.display.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.display.grid_columnconfigure(0, weight=1)

        # Lista de processos armazenados
        self.processos = []
        self.processo_id = 1

    def add_processo(self):
        try:
            tempo_exec = int(self.execucaoIn.get())
        except ValueError:
            tempo_exec = 0
        quantum = self.quantumIn.get()


        cor = f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"


        # Cria processo
        processo = {
            "pid": f"P{self.processo_id}",
            "exec": tempo_exec,
            "quantum": quantum,
            "cor": cor 
        }
        self.processos.append(processo)
        self.processo_id += 1



        # Mostra no frame
        self._criar_item_display(processo, f"{processo['pid']} | Exec: {tempo_exec} | Quantum: {quantum}")

        # Limpa entrada
        self.execucaoIn.delete(0, "end")




    def simular(self):
        # Limpa área de exibição
        for widget in self.display.winfo_children():
            widget.destroy()



        # Exemplo: só exibe em ordem (a lógica do algoritmo você coloca depois)
        for i, p in enumerate(self.processos, start=1):
            texto = f"Execução {i}: {p['pid']} (tempo {p['exec']})"
            self._criar_item_display(p, texto)





    def _criar_item_display(self, processo, texto):
        item = ctk.CTkFrame(self.display, corner_radius=20)
        item.pack(fill="x", pady=5, padx=5)

        bola = ctk.CTkLabel(item, text="●", text_color=processo["cor"], font=("Arial", 28))
        bola.pack(side="left", padx=10, pady=(0,5))

        info = ctk.CTkLabel(item, text=texto)
        info.pack(side="left", padx=17)



if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = Principal()
    app.mainloop()
