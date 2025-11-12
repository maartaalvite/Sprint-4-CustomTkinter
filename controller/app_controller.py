from model.usuario_model import Usuario, GestorUsuarios
from view.main_view import MainView
from view.alta_usuario_modal import AltaUsuarioModal


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
            self.cargar,
            self.buscar,
            self.editar_usuario
        )

        # Cargar al inicio
        self.cargar(inicial=True)
        self.vista.set_estado(" Aplicación lista.")

    # --- Refrescar lista ---
    def refrescar_lista(self):
        usuarios = self.modelo.listar()
        self.vista.set_lista(usuarios)
        self.vista.set_estado(f"{len(usuarios)} usuario(s) en la lista.")

    # --- Alta ---
    def alta_usuario_modal(self):
        AltaUsuarioModal(self.root, self.confirmar_alta, self.avatars)

    def confirmar_alta(self, nombre, edad, genero, avatar):
        try:
            nuevo = Usuario(nombre, edad, genero, avatar)
            self.modelo.añadir(nuevo)
            self.refrescar_lista()
            self.vista.set_estado(f" Usuario '{nombre}' añadido correctamente.")
        except Exception as e:
            self.vista.set_estado(f" Error al añadir usuario: {e}")

    # --- Edición ---
    def editar_usuario(self, indice):
        usuarios = self.modelo.listar()
        if 0 <= indice < len(usuarios):
            usuario = usuarios[indice]
            AltaUsuarioModal(
                self.root,
                lambda n, e, g, a: self.confirmar_edicion(indice, n, e, g, a),
                self.avatars
            )
            self.vista.set_estado(f" Editando a {usuario.nombre}...")
        else:
            self.vista.set_estado(" No se pudo editar (índice inválido).")

    def confirmar_edicion(self, indice, nombre, edad, genero, avatar):
        try:
            actualizado = Usuario(nombre, edad, genero, avatar)
            self.modelo.actualizar(indice, actualizado)
            self.refrescar_lista()
            self.vista.set_estado(f" Usuario '{nombre}' actualizado correctamente.")
        except Exception as e:
            self.vista.set_estado(f" Error al actualizar: {e}")

    # --- Buscar / Filtrar ---
    def buscar(self, texto, genero):
        try:
            resultado = self.modelo.filtrar(texto, genero)
            self.vista.set_lista(resultado)
            self.vista.set_estado(f" {len(resultado)} usuario(s) encontrados.")
        except Exception as e:
            self.vista.set_estado(f" Error en la búsqueda: {e}")

    # --- Guardar / Cargar ---
    def guardar(self):
        try:
            self.modelo.guardar_csv()
            self.vista.set_estado(" Usuarios guardados correctamente.")
        except Exception as e:
            self.vista.set_estado(f" Error al guardar: {e}")

    def cargar(self, inicial=False):
        try:
            self.modelo.cargar_csv()
            self.refrescar_lista()
            if inicial:
                self.vista.set_estado(" Usuarios cargados al iniciar.")
            else:
                self.vista.set_estado(" Usuarios cargados correctamente.")
        except FileNotFoundError:
            self.vista.set_estado(" No se encontró el archivo CSV (se creará al guardar).")
        except Exception as e:
            self.vista.set_estado(f" Error al cargar: {e}")

    # --- Salir ---
    def salir(self):
        try:
            self.guardar()
            self.vista.set_estado(" Cambios guardados. Cerrando aplicación...")
        except Exception:
            self.vista.set_estado(" Saliendo sin guardar por error inesperado.")
        self.root.quit()
