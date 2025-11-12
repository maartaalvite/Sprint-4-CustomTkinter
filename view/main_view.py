import customtkinter as ctk
from PIL import Image
import tkinter as tk


class MainView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # Callbacks
        self._callback_añadir = None
        self._callback_salir = None
        self._callback_guardar = None
        self._callback_cargar = None
        self._callback_buscar = None
        self._callback_editar = None

        self.usuarios = []
        self.usuario_seleccionado = None

        self.crear_menu(master)
        self.crear_widgets()

    def crear_menu(self, master):
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Guardar", command=self._on_guardar_click)
        menu_archivo.add_command(label="Cargar", command=self._on_cargar_click)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self._on_salir_click)

    def crear_widgets(self):
        # --- Filtros y búsqueda ---
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(fill="x", padx=10, pady=5)

        self.entry_buscar = ctk.CTkEntry(frame_filtros, placeholder_text="Buscar por nombre...")
        self.entry_buscar.pack(side="left", fill="x", expand=True, padx=5)

        self.combo_genero = ctk.CTkOptionMenu(frame_filtros, values=["Todos", "Masculino", "Femenino", "Otro"])
        self.combo_genero.pack(side="left", padx=5)

        self.btn_buscar = ctk.CTkButton(frame_filtros, text="Buscar", width=100, command=self._on_buscar_click)
        self.btn_buscar.pack(side="left", padx=5)

        self.btn_añadir = ctk.CTkButton(frame_filtros, text="Añadir usuario", command=self._on_añadir_click)
        self.btn_añadir.pack(side="left", padx=5)

        # --- Contenedor principal ---
        contenedor = ctk.CTkFrame(self)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Lista de usuarios ---
        self.lista = tk.Listbox(contenedor, height=15, activestyle="none")
        self.lista.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.lista.bind("<ButtonRelease-1>", self._on_seleccionar_usuario)
        self.lista.bind("<Double-1>", self._on_doble_click)

        # --- Panel lateral de detalles ---
        self.panel_detalles = ctk.CTkFrame(contenedor, width=250)
        self.panel_detalles.pack(side="right", fill="y")

        ctk.CTkLabel(self.panel_detalles, text="Detalles del usuario", font=("Arial", 16, "bold")).pack(pady=(10, 5))

        self.lbl_avatar = ctk.CTkLabel(self.panel_detalles, text="(sin avatar)")
        self.lbl_avatar.pack(pady=10)

        self.lbl_nombre = ctk.CTkLabel(self.panel_detalles, text="Nombre: -")
        self.lbl_nombre.pack(pady=5)

        self.lbl_edad = ctk.CTkLabel(self.panel_detalles, text="Edad: -")
        self.lbl_edad.pack(pady=5)

        self.lbl_genero = ctk.CTkLabel(self.panel_detalles, text="Género: -")
        self.lbl_genero.pack(pady=5)

        # --- Barra de estado ---
        self.label_estado = ctk.CTkLabel(self, text="Listo", anchor="w")
        self.label_estado.pack(fill="x", padx=10, pady=5)

    # ---- Callbacks configurables ----
    def configurar_callbacks(self, on_añadir, on_salir, on_guardar, on_cargar, on_buscar, on_editar):
        self._callback_añadir = on_añadir
        self._callback_salir = on_salir
        self._callback_guardar = on_guardar
        self._callback_cargar = on_cargar
        self._callback_buscar = on_buscar
        self._callback_editar = on_editar

    # ---- Eventos internos ----
    def _on_añadir_click(self):
        if self._callback_añadir:
            self._callback_añadir()

    def _on_salir_click(self):
        if self._callback_salir:
            self._callback_salir()

    def _on_guardar_click(self):
        if self._callback_guardar:
            self._callback_guardar()

    def _on_cargar_click(self):
        if self._callback_cargar:
            self._callback_cargar()

    def _on_buscar_click(self):
        if self._callback_buscar:
            texto = self.entry_buscar.get()
            genero = self.combo_genero.get()
            self._callback_buscar(texto, genero)

    def _on_doble_click(self, event):
        if self._callback_editar:
            try:
                index = self.lista.curselection()[0]
                self._callback_editar(index)
            except Exception:
                pass

    def _on_seleccionar_usuario(self, event):
        try:
            index = self.lista.curselection()[0]
            usuario = self.usuarios[index]
            self.mostrar_detalles(usuario)
        except Exception:
            pass

    # ---- Métodos de vista ----
    def set_lista(self, usuarios):
        self.usuarios = usuarios
        self.lista.delete(0, "end")
        for i, u in enumerate(usuarios):
            self.lista.insert("end", f"{u.nombre} ({u.edad} años, {u.genero})")
        self.set_estado(f"{len(usuarios)} usuarios cargados.")

    def mostrar_detalles(self, usuario):
        self.usuario_seleccionado = usuario
        self.lbl_nombre.configure(text=f"Nombre: {usuario.nombre}")
        self.lbl_edad.configure(text=f"Edad: {usuario.edad}")
        self.lbl_genero.configure(text=f"Género: {usuario.genero}")

        if usuario.avatar:
            try:
                img = ctk.CTkImage(light_image=Image.open(usuario.avatar), size=(96, 96))
                self.lbl_avatar.configure(image=img, text="")
                self.lbl_avatar.image = img
            except Exception:
                self.lbl_avatar.configure(text="[Error cargando avatar]", image=None)
        else:
            self.lbl_avatar.configure(text="(sin avatar)", image=None)

    def set_estado(self, texto):
        self.label_estado.configure(text=texto)
