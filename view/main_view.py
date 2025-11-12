# view/main_view.py
import customtkinter as ctk

class MainView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        # Layout: izquierda (lista), derecha (detalle), abajo (barra estado)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # --- Lista de usuarios ---
        frame_lista = ctk.CTkScrollableFrame(self)
        frame_lista.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.lista_usuarios = frame_lista

        self.labels_usuarios = []

        # --- Panel de previsualización ---
        frame_preview = ctk.CTkFrame(self)
        frame_preview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.lbl_avatar = ctk.CTkLabel(frame_preview, text="[Sin imagen]", width=150, height=150)
        self.lbl_avatar.pack(pady=10)

        self.lbl_detalles = ctk.CTkLabel(frame_preview, text="Selecciona un usuario", anchor="w", justify="left")
        self.lbl_detalles.pack(padx=10, pady=10, fill="x")

        # --- Barra de estado ---
        self.lbl_estado = ctk.CTkLabel(self, text="Listo", anchor="w")
        self.lbl_estado.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    def set_lista(self, usuarios):
        # Limpiar
        for lbl in self.labels_usuarios:
            lbl.destroy()
        self.labels_usuarios.clear()

        # Crear etiquetas
        for i, usuario in enumerate(usuarios):
            lbl = ctk.CTkLabel(self.lista_usuarios, text=str(usuario), anchor="w")
            lbl.pack(fill="x", padx=5, pady=2)
            self.labels_usuarios.append(lbl)

    def mostrar_usuario(self, usuario):
        self.lbl_detalles.configure(text=f"Nombre: {usuario.nombre}\nEdad: {usuario.edad}\nGénero: {usuario.genero}")

    def set_estado(self, texto):
        self.lbl_estado.configure(text=texto)
