import customtkinter as ctk
from PIL import Image
from tkinter import messagebox


class AltaUsuarioModal(ctk.CTkToplevel):
    def __init__(self, master, callback_guardar, avatars):
        super().__init__(master)
        self.callback_guardar = callback_guardar
        self.avatars = avatars
        self.avatar_seleccionado = avatars[0] if avatars else None

        self.title("Alta / Edición de usuario")
        self.geometry("400x500")
        self.resizable(False, False)
        self.grab_set()  # bloquea ventana principal

        self.crear_widgets()

    def crear_widgets(self):
        # ---- Campos de texto ----
        ctk.CTkLabel(self, text="Nombre:").pack(pady=(10, 0))
        self.entry_nombre = ctk.CTkEntry(self, width=250)
        self.entry_nombre.pack(pady=5)

        ctk.CTkLabel(self, text="Edad (0–100):").pack(pady=(10, 0))
        self.entry_edad = ctk.CTkEntry(self, width=100)
        self.entry_edad.pack(pady=5)

        ctk.CTkLabel(self, text="Género:").pack(pady=(10, 0))
        self.var_genero = ctk.StringVar(value="Masculino")
        frame_genero = ctk.CTkFrame(self)
        frame_genero.pack(pady=5)
        for g in ["Masculino", "Femenino", "Otro"]:
            ctk.CTkRadioButton(frame_genero, text=g, variable=self.var_genero, value=g).pack(side="left", padx=5)

        # ---- Avatares con imagen ----
        ctk.CTkLabel(self, text="Selecciona un avatar:").pack(pady=(10, 0))
        frame_avatars = ctk.CTkFrame(self)
        frame_avatars.pack(pady=5)

        self.botones_avatar = []
        for ruta in self.avatars:
            try:
                img = ctk.CTkImage(light_image=Image.open(ruta), size=(64, 64))
                btn = ctk.CTkButton(frame_avatars, image=img, text="", width=70, height=70,
                                     command=lambda r=ruta: self.seleccionar_avatar(r))
                btn.pack(side="left", padx=5)
                btn.image = img  # mantener referencia
                self.botones_avatar.append(btn)
            except Exception:
                continue  # ignora avatares faltantes

        # ---- Confirmar ----
        ctk.CTkButton(self, text="Confirmar", command=self.guardar).pack(pady=15)

    def seleccionar_avatar(self, ruta):
        self.avatar_seleccionado = ruta
        for b in self.botones_avatar:
            b.configure(fg_color="transparent")
        # Marcar visualmente el botón seleccionado
        for b in self.botones_avatar:
            if getattr(b, "image", None) and ruta in b.image._light_image.filename:
                b.configure(fg_color="green")

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        edad_txt = self.entry_edad.get().strip()
        genero = self.var_genero.get()
        avatar = self.avatar_seleccionado

        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        if not edad_txt.isdigit():
            messagebox.showerror("Error", "La edad debe ser un número.")
            return

        edad = int(edad_txt)
        self.callback_guardar(nombre, edad, genero, avatar)
        self.destroy()
