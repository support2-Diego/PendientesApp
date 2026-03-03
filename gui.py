import customtkinter as ctk
from tkcalendar import DateEntry
from database import Database
from logic import TaskLogic

class TareaCard(ctk.CTkFrame):
    def __init__(self, master, id_tarea, titulo, descripcion, prioridad, fecha, color_urgencia, al_completar):
        # El borde de la tarjeta indica la URGENCIA (Fecha)
        super().__init__(master, border_width=2, border_color=color_urgencia)
        self.columnconfigure(0, weight=1)
        
        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text=titulo, font=("Arial", 16, "bold"), anchor="w")
        self.lbl_titulo.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        # Descripción Detallada
        self.txt_desc = ctk.CTkTextbox(self, height=45, font=("Arial", 11), fg_color="transparent", border_width=0)
        self.txt_desc.insert("0.0", descripcion if descripcion else "Sin descripción.")
        self.txt_desc.configure(state="disabled")
        self.txt_desc.grid(row=1, column=0, padx=10, pady=2, sticky="ew")
        
        # --- CUADRO DE PRIORIDAD ---
        color_prio = TaskLogic.obtener_color_prioridad(prioridad)
        self.frame_prio = ctk.CTkFrame(self, fg_color=color_prio, corner_radius=4)
        self.frame_prio.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        
        self.lbl_prio = ctk.CTkLabel(self.frame_prio, text=" PRIORIDAD ", text_color="white", font=("Arial", 10, "bold"))
        self.lbl_prio.pack(padx=5, pady=2)

        # Fecha de entrega al lado
        self.lbl_fecha = ctk.CTkLabel(self, text=f"Fecha: {fecha}", font=("Arial", 11, "italic"))
        self.lbl_fecha.grid(row=2, column=0, padx=(100, 10), pady=(0, 10), sticky="w")
        
        # Botón Completar
        self.btn_done = ctk.CTkButton(self, text="✓", width=35, height=35, fg_color="#2FA572", 
                                      command=lambda: al_completar(id_tarea))
        self.btn_done.grid(row=0, column=1, rowspan=3, padx=15)

class AppGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("Gestor de Tareas")
        self.geometry("850x600")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # PANEL IZQUIERDO (Formulario)
        self.form_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.form_frame.grid(row=0, column=0, sticky="nsew")
        self.form_frame.grid_propagate(False)

        ctk.CTkLabel(self.form_frame, text="Nueva Tarea", font=("Arial", 20, "bold")).pack(pady=20)
        
        ctk.CTkLabel(self.form_frame, text="Título:", anchor="w").pack(fill="x", padx=20)
        self.entry_tarea = ctk.CTkEntry(self.form_frame)
        self.entry_tarea.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Descripción:", anchor="w").pack(fill="x", padx=20)
        self.entry_desc = ctk.CTkTextbox(self.form_frame, height=80)
        self.entry_desc.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Prioridad:", anchor="w").pack(fill="x", padx=20)
        self.combo_prioridad = ctk.CTkOptionMenu(self.form_frame, values=["1 - Alta", "2 - Media", "3 - Baja"])
        self.combo_prioridad.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Fecha:", anchor="w").pack(fill="x", padx=20)
        self.cal = DateEntry(self.form_frame, date_pattern='y-mm-dd')
        self.cal.pack(fill="x", padx=20, pady=(0, 20))

        self.btn_guardar = ctk.CTkButton(self.form_frame, text="Guardar", command=self.agregar_tarea)
        self.btn_guardar.pack(fill="x", padx=20, pady=10)

        # PANEL DERECHO (Lista ordenada por SQL)
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Mis Pendientes")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.actualizar_lista()

    def agregar_tarea(self):
        tarea = self.entry_tarea.get()
        descripcion = self.entry_desc.get("1.0", "end-1c")
        prioridad = int(self.combo_prioridad.get()[0])
        fecha = self.cal.get_date().strftime("%Y-%m-%d")

        if TaskLogic.validar_datos(tarea)[0]:
            self.db.insertar_tarea(tarea, descripcion, prioridad, fecha)
            self.entry_tarea.delete(0, 'end')
            self.entry_desc.delete("1.0", "end")
            self.actualizar_lista()

    def actualizar_lista(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for t in self.db.obtener_tareas():
            # t[0]=id, t[1]=tarea, t[2]=descripcion, t[3]=prioridad, t[4]=fecha
            urgencia, color_borde = TaskLogic.calcular_urgencia(t[4])
            card = TareaCard(self.list_frame, t[0], t[1], t[2], t[3], t[4], color_borde, self.completar_tarea)
            card.pack(fill="x", padx=5, pady=5)

    def completar_tarea(self, id_tarea):
        self.db.marcar_completada(id_tarea)
        self.actualizar_lista()