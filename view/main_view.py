import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import messagebox


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
        self._callback_toggle_auto_guardado = None
        self._callback_eliminar = None

        self.usuarios = []
        self.usuario_seleccionado = None

        self.crear_menu(master)
        self.crear_widgets()

    def crear_menu(self, master):
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        # Menú del archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Guardar", command=self._on_guardar_click)
        menu_archivo.add_command(label="Cargar", command=self._on_cargar_click)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self._on_salir_click)

        # Menú de ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self._on_acerca_de_click)

    def crear_widgets(self):
        #  Barrita superior con búsqueda y filtros
        frame_superior = ctk.CTkFrame(self)
        frame_superior.pack(fill="x", padx=10, pady=5)

        # Búsqueda
        ctk.CTkLabel(frame_superior, text="Buscar:").pack(side="left", padx=(0, 5))
        self.entry_buscar = ctk.CTkEntry(frame_superior, placeholder_text="Nombre...", width=150)
        self.entry_buscar.pack(side="left", padx=5)

        # Género
        ctk.CTkLabel(frame_superior, text="Género:").pack(side="left", padx=(20, 5))
        self.combo_genero = ctk.CTkOptionMenu(frame_superior, values=["Todos", "Masculino", "Femenino", "Otro"],
                                              width=120)
        self.combo_genero.pack(side="left", padx=5)

        # Botones
        self.btn_eliminar = ctk.CTkButton(frame_superior, text="Eliminar", width=80, command=self._on_eliminar_click)
        self.btn_eliminar.pack(side="left", padx=(20, 5))

        self.btn_añadir = ctk.CTkButton(frame_superior, text="Añadir", width=80, command=self._on_añadir_click)
        self.btn_añadir.pack(side="left", padx=5)

        #  Contenedor principal
        contenedor_principal = ctk.CTkFrame(self)
        contenedor_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel izquierdo con la lista de users
        frame_lista = ctk.CTkFrame(contenedor_principal)
        frame_lista.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(frame_lista, text="Lista de Usuarios", font=("Arial", 14, "bold")).pack(pady=10)

        self.lista = tk.Listbox(frame_lista, height=20, activestyle="none", font=("Arial", 11))
        self.lista.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.lista.bind("<ButtonRelease-1>", self._on_seleccionar_usuario)
        self.lista.bind("<Double-1>", self._on_doble_click)

        # Panel derecho con datos del user
        frame_detalles = ctk.CTkFrame(contenedor_principal, width=300)
        frame_detalles.pack(side="right", fill="y")
        frame_detalles.pack_propagate(False)  # Mantener el ancho fijo

        ctk.CTkLabel(frame_detalles, text="Detalles del Usuario", font=("Arial", 16, "bold")).pack(pady=20)

        # Avatar
        self.lbl_avatar = ctk.CTkLabel(frame_detalles, text="(sin avatar)", width=100, height=100)
        self.lbl_avatar.pack(pady=10)

        # Campos para la info
        frame_info = ctk.CTkFrame(frame_detalles)
        frame_info.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_info, text="Nombre:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.lbl_nombre = ctk.CTkLabel(frame_info, text="-", font=("Arial", 11))
        self.lbl_nombre.pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(frame_info, text="Edad:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.lbl_edad = ctk.CTkLabel(frame_info, text="-", font=("Arial", 11))
        self.lbl_edad.pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(frame_info, text="Género:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.lbl_genero = ctk.CTkLabel(frame_info, text="-", font=("Arial", 11))
        self.lbl_genero.pack(anchor="w", pady=(0, 10))

        #  Barra inferior
        frame_estado = ctk.CTkFrame(self)
        frame_estado.pack(fill="x", padx=10, pady=5)

        # Estado general
        self.label_estado = ctk.CTkLabel(frame_estado, text="Listo", anchor="w")
        self.label_estado.pack(side="left", fill="x", expand=True)

        # Auto guardado
        self.btn_auto_guardado = ctk.CTkButton(
            frame_estado,
            text="Auto guardar (10s): OFF",
            command=self._on_toggle_auto_guardado_click,
            fg_color="gray",
            hover_color="dark gray",
            width=180
        )
        self.btn_auto_guardado.pack(side="right")

    #Callbacks configurables
    def configurar_callbacks(self, on_añadir, on_salir, on_guardar, on_cargar, on_buscar, on_editar,
                             on_toggle_auto_guardado, on_eliminar):
        self._callback_añadir = on_añadir
        self._callback_salir = on_salir
        self._callback_guardar = on_guardar
        self._callback_cargar = on_cargar
        self._callback_buscar = on_buscar
        self._callback_editar = on_editar
        self._callback_toggle_auto_guardado = on_toggle_auto_guardado
        self._callback_eliminar = on_eliminar

    #Eventos con click
    def _on_añadir_click(self):
        if self._callback_añadir:
            self._callback_añadir()

    def _on_eliminar_click(self):
        if self._callback_eliminar:
            try:
                index = self.lista.curselection()[0]
                self._callback_eliminar(index)
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar")

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

    def _on_toggle_auto_guardado_click(self):
        if self._callback_toggle_auto_guardado:
            self._callback_toggle_auto_guardado()

    def _on_acerca_de_click(self):
        messagebox.showinfo(
            "Acerca de",
            "Registro de Usuarios\n\n"
            "Aplicación desarrollada con:\n"
            "- CustomTkinter\n"
            "- Arquitectura MVC\n"
            "- Persistencia en CSV\n\n"
            "Funcionalidades:\n"
            "- Alta, baja y modificación de usuarios\n"
            "- Búsqueda y filtrado\n"
            "- Auto-guardado cada 10 segundos"
        )

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

    #Métodos de la vista
    def set_lista(self, usuarios):
        self.usuarios = usuarios
        self.lista.delete(0, "end")
        for i, u in enumerate(usuarios):
            self.lista.insert("end", f"{u.nombre} ({u.edad} años, {u.genero})")

        # Actualizar el  contador en la barrita
        self.set_estado(f"{len(usuarios)} usuarios cargados")

    def mostrar_detalles(self, usuario):
        self.usuario_seleccionado = usuario
        self.lbl_nombre.configure(text=usuario.nombre)
        self.lbl_edad.configure(text=f"{usuario.edad} años")
        self.lbl_genero.configure(text=usuario.genero)

        if usuario.avatar:
            try:
                img = ctk.CTkImage(light_image=Image.open(usuario.avatar), size=(100, 100))
                self.lbl_avatar.configure(image=img, text="")
                self.lbl_avatar.image = img
            except Exception:
                self.lbl_avatar.configure(text="[Error cargando avatar]", image=None)
        else:
            self.lbl_avatar.configure(text="(sin avatar)", image=None)

    def set_estado(self, texto):
        self.label_estado.configure(text=texto)

    def actualizar_boton_auto_guardado(self, activo):
        """Actualiza la apariencia del botón de auto-guardado"""
        if activo:
            self.btn_auto_guardado.configure(
                text="Auto guardar (10s): ON",
                fg_color="#28a745",
                hover_color="#218838"
            )
        else:
            self.btn_auto_guardado.configure(
                text="Auto guardar (10s): OFF",
                fg_color="gray",
                hover_color="dark gray"
            )