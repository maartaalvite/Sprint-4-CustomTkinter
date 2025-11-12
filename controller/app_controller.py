from model.usuario_model import Usuario, GestorUsuarios
from view.main_view import MainView, AltaUsuarioModal

class AppController:
    def __init__(self, root):
        self.root = root
        self.modelo = GestorUsuarios()
        self.vista = MainView(root)

        self.avatars = ["assets/avatar1.png", "assets/avatar2.png", "assets/avatar3.png"]

        # Configurar callbacks
        self.vista.configurar_callbacks(
            self.alta_usuario_modal,
            self.salir,
            self.guardar,
            self.cargar
        )

        # Intentar cargar usuarios previos
        self.cargar(inicial=True)

    def refrescar_lista(self):
        usuarios = self.modelo.listar()
        self.vista.set_lista(usuarios)
        if usuarios:
            self.vista.mostrar_usuario(usuarios[-1])

    # --- Alta ---
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

    # --- CSV ---
    def guardar(self):
        try:
            self.modelo.guardar_csv()
            self.vista.set_estado("Usuarios guardados correctamente.")
        except Exception as e:
            self.vista.set_estado(f"Error al guardar: {e}")

    def cargar(self, inicial=False):
        try:
            self.modelo.cargar_csv()
            self.refrescar_lista()
            if not inicial:
                self.vista.set_estado("Usuarios cargados correctamente.")
        except Exception as e:
            self.vista.set_estado(f"Error al cargar: {e}")

    # --- Salir ---
    def salir(self):
        self.guardar()
        self.root.quit()
