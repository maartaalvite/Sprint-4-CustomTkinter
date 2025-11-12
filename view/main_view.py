import customtkinter as ctk
from PIL import Image
import tkinter as tk


class MainView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self._callback_añadir = None
        self._callback_salir = None
        self._callback_guardar = None
        self._callback_cargar = None
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
        # Layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # --- Botonera superior ---
        frame_botones = ctk.CTkFrame(self)
        frame_botones.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0))
        frame_botones.grid_columnconfigure((0, 1), weight=1)

        self.btn_añadir = ctk.CTkButton(frame_botones, text="Añadir Usuario", command=self._on_añadir_click)
        self.btn_añadir.grid(row=0, column=0, padx=5, pady=5)

        self.btn_salir = ctk.CTkButton(frame_botones, text="Salir", command=self._on_salir_click)
        self.btn_salir.grid(row=0, column=1, padx=5, pady=5)

        # --- Zona lista ---
        frame_lista = ctk.CTkScrollableFrame(self)
        frame_lista.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.lista_usuarios = frame_lista
        self.labels_usuarios = []

        # --- Zona de previsualización ---
        frame_preview = ctk.CTkFrame(self)
        frame_preview.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.lbl_avatar = ctk.CTkLabel(frame_preview, text="[Sin imagen]", width=150, height=150)
        self.lbl_avatar.pack(pady=10)

        self.lbl_detalles = ctk.CTkLabel(frame_preview, text="Selecciona un usuario", anchor="w", justify="left")
        self.lbl_detalles.pack(padx=10, pady=10, fill="x")

        # --- Barra de estado ---
        self.lbl_estado = ctk.CTkLabel(self, text="Listo", anchor="w")
        self.lbl_estado.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    # ---- Callbacks configurables ----
    def configurar_callbacks(self, on_añadir, on_salir, on_guardar, on_cargar):
        self._callback_añadir = on_añadir
        self._callback_salir = on_salir
        self._callback_guardar = on_guardar
        self._callback_cargar = on_cargar

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

    # ---- Métodos de vista ----
    def set_lista(self, usuarios):
        for lbl in self.labels_usuarios:
            lbl.destroy()
        self.labels_usuarios.clear()

        for i, usuario in enumerate(usuarios):
            lbl = ctk.CTkLabel(self.lista_usuarios, text=str(usuario), anchor="w")
            lbl.pack(fill="x", padx=5, pady=2)
            self.labels_usuarios.append(lbl)

    def mostrar_usuario(self, usuario):
        self.lbl_detalles.configure(text=f"Nombre: {usuario.nombre}\nEdad: {usuario.edad}\nGénero: {usuario.genero}")
        if usuario.avatar:
            try:
                img = ctk.CTkImage(light_image=Image.open(usuario.avatar), size=(96, 96))
                self.lbl_avatar.configure(image=img, text="")
                self.lbl_avatar.image = img  # mantener referencia
            except Exception:
                self.lbl_avatar.configure(text="[Error cargando avatar]", image=None)
        else:
            self.lbl_avatar.configure(text="[Sin imagen]", image=None)

    def set_estado(self, texto):
        self.lbl_estado.configure(text=texto)


# ---- Ventana modal de alta ----
class AltaUsuarioModal(ctk.CTkToplevel):
    def __init__(self, master, callback_confirmar, lista_avatars):
        super().__init__(master)
        self.title("Nuevo Usuario")
        self.geometry("400x400")
        self.resizable(False, False)
        self.grab_set()  # modal
        self.callback_confirmar = callback_confirmar
        self.lista_avatars = lista_avatars
        self.avatar_seleccionado = lista_avatars[0]
        self.crear_widgets()

    def crear_widgets(self):
        ctk.CTkLabel(self, text="Nombre:").pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(self, width=250)
        self.entry_nombre.pack(pady=5)

        ctk.CTkLabel(self, text="Edad (0-100):").pack(pady=5)
        self.entry_edad = ctk.CTkEntry(self, width=100)
        self.entry_edad.pack(pady=5)

        ctk.CTkLabel(self, text="Género:").pack(pady=5)
        self.var_genero = ctk.StringVar(value="Masculino")
        frame_genero = ctk.CTkFrame(self)
        frame_genero.pack(pady=5)
        for g in ["Masculino", "Femenino", "Otro"]:
            ctk.CTkRadioButton(frame_genero, text=g, variable=self.var_genero, value=g).pack(side="left", padx=5)

        ctk.CTkLabel(self, text="Selecciona avatar:").pack(pady=5)
        frame_avatars = ctk.CTkFrame(self)
        frame_avatars.pack(pady=5)
        self.botones_avatar = []
        from PIL import Image
        for ruta in self.lista_avatars:
            img = ctk.CTkImage(light_image=Image.open(ruta), size=(64, 64))
            btn = ctk.CTkButton(frame_avatars, image=img, text="", width=70, height=70,
                                 command=lambda r=ruta: self.seleccionar_avatar(r))
            btn.pack(side="left", padx=5)
            btn.image = img
            self.botones_avatar.append(btn)

        ctk.CTkButton(self, text="Confirmar", command=self.confirmar).pack(pady=15)

    def seleccionar_avatar(self, ruta):
        self.avatar_seleccionado = ruta
        for b in self.botones_avatar:
            b.configure(fg_color="transparent")
        # marcar visualmente el elegido
        self.focus()

    def confirmar(self):
        nombre = self.entry_nombre.get().strip()
        edad_texto = self.entry_edad.get().strip()
        genero = self.var_genero.get()
        avatar = self.avatar_seleccionado

        try:
            edad = int(edad_texto)
        except ValueError:
            edad = -1

        self.callback_confirmar(nombre, edad, genero, avatar)
        self.destroy()
