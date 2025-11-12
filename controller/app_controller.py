from model.usuario_model import Usuario, GestorUsuarios
from view.main_view import MainView, AltaUsuarioModal

class AppController:
    def __init__(self, root):
        self.root = root
        self.modelo = GestorUsuarios()
        self.vista = MainView(root)

        # lista de imágenes disponibles
        self.avatars = ["assets/avatar1.png", "assets/avatar2.png", "assets/avatar3.png"]

        # Configurar callbacks
        self.vista.configurar_callbacks(self.alta_usuario_modal, self.salir)

        # Datos iniciales opcionales
        self.modelo.añadir(Usuario("Ana", 25, "Femenino", self.avatars[0]))
        self.modelo.añadir(Usuario("Luis", 32, "Masculino", self.avatars[1]))
        self.refrescar_lista()

        self.vista.set_estado("Aplicación iniciada")

    def refrescar_lista(self):
        usuarios = self.modelo.listar()
        self.vista.set_lista(usuarios)
        if usuarios:
            self.vista.mostrar_usuario(usuarios[-1])

    # --- Alta de usuario ---
    def alta_usuario_modal(self):
        AltaUsuarioModal(self.root, self.confirmar_alta, self.avatars)

    def confirmar_alta(self, nombre, edad, genero, avatar):
        try:
            nuevo = Usuario(nombre, edad, genero, avatar)
            self.modelo.añadir(nuevo)
            self.refrescar_lista()
            self.vista.set_estado(f"Usuario {nombre} añadido correctamente.")
        except Exception as e:
            self.vista.set_estado(f"Error: {e}")

    # --- Salir ---
    def salir(self):
        self.root.quit()
