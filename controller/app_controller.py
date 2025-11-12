# controller/app_controller.py
from model.usuario_model import Usuario, GestorUsuarios
from view.main_view import MainView

class AppController:
    def __init__(self, root):
        self.root = root
        self.modelo = GestorUsuarios()
        self.vista = MainView(root)

        # Datos de ejemplo
        self.modelo.añadir(Usuario("Ana", 25, "Femenino"))
        self.modelo.añadir(Usuario("Luis", 32, "Masculino"))

        self.refrescar_lista()

        self.vista.set_estado("Aplicación iniciada")

    def refrescar_lista(self):
        usuarios = self.modelo.listar()
        self.vista.set_lista(usuarios)
