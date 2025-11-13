import threading
import time
from model.usuario_model import Usuario, GestorUsuarios
from view.main_view import MainView
from view.alta_usuario_modal import AltaUsuarioModal
from tkinter import messagebox


class AppController:
    def __init__(self, root):
        self.root = root
        self.modelo = GestorUsuarios()
        self.vista = MainView(root)
        self.avatars = ["assets/avatar1.png", "assets/avatar2.png", "assets/avatar3.png"]

        # Variables para el auto-guardado
        self.auto_guardado_activo = False
        self.hilo_auto_guardado = None
        self.detener_hilo = False

        # Configurar los callbacks
        self.vista.configurar_callbacks(
            self.alta_usuario_modal,
            self.salir,
            self.guardar,
            self.cargar,
            self.buscar,
            self.editar_usuario,
            self.toggle_auto_guardado,
            self.eliminar_usuario
        )

        # Configurar los eventos de búsqueda en tiempo real
        self.vista.entry_buscar.bind("<KeyRelease>", self._on_busqueda_change)
        self.vista.combo_genero.configure(command=self._on_filtro_change)

        # Cargar al inicio
        self.cargar(inicial=True)
        self.vista.set_estado("Listo")

    #Para la búsqueda en tiempo real
    def _on_busqueda_change(self, event=None):
        self.buscar()

    def _on_filtro_change(self, choice):
        self.buscar()

    # Refrescar la lista
    def refrescar_lista(self):
        usuarios = self.modelo.listar()
        self.vista.set_lista(usuarios)

    #Auto-guardado con threads
    def toggle_auto_guardado(self):
        if not self.auto_guardado_activo:
            self.iniciar_auto_guardado()
        else:
            self.detener_auto_guardado()

    def iniciar_auto_guardado(self):
        """Inicia el hilo de auto-guardado"""
        self.auto_guardado_activo = True
        self.detener_hilo = False
        self.hilo_auto_guardado = threading.Thread(target=self._ciclo_auto_guardado, daemon=True)
        self.hilo_auto_guardado.start()
        self.vista.set_estado("Auto-guardado ACTIVADO (cada 10 segundos)")
        self.vista.actualizar_boton_auto_guardado(True)

    def detener_auto_guardado(self):
        """Detiene el hilo de auto-guardado"""
        self.auto_guardado_activo = False
        self.detener_hilo = True
        if self.hilo_auto_guardado and self.hilo_auto_guardado.is_alive():
            self.hilo_auto_guardado.join(timeout=2.0)
        self.vista.set_estado("Auto-guardado DESACTIVADO")
        self.vista.actualizar_boton_auto_guardado(False)

    def _ciclo_auto_guardado(self):
        """Ciclo principal del auto-guardado (se ejecuta en hilo separado)"""
        while not self.detener_hilo:
            time.sleep(10)  # Espera 10 segundos
            if self.detener_hilo:
                break
            # Usar after() para ejecutar en el hilo principal de Tkinter
            self.root.after(0, self._auto_guardar)

    def _auto_guardar(self):
        """Ejecuta el guardado (llamado desde el hilo principal)"""
        if self.auto_guardado_activo and not self.detener_hilo:
            try:
                self.modelo.guardar_csv()
                self.vista.set_estado(f"Auto-guardado: {time.strftime('%H:%M:%S')} - Datos guardados")
            except Exception as e:
                self.vista.set_estado(f"Error en auto-guardado: {e}")

    # Dar de alta
    def alta_usuario_modal(self):
        AltaUsuarioModal(self.root, self.confirmar_alta, self.avatars)

    def confirmar_alta(self, nombre, edad, genero, avatar):
        try:
            nuevo = Usuario(nombre, edad, genero, avatar)
            self.modelo.añadir(nuevo)
            self.refrescar_lista()
            self.vista.set_estado(f"Usuario '{nombre}' añadido correctamente")
        except Exception as e:
            self.vista.set_estado(f"Error al añadir usuario: {e}")

    #Eliminar usuario
    def eliminar_usuario(self, indice):
        usuarios = self.modelo.listar()
        if 0 <= indice < len(usuarios):
            usuario = usuarios[indice]
            if messagebox.askyesno("Confirmar", f"¿Eliminar a {usuario.nombre}?"):
                try:
                    self.modelo.eliminar(indice)
                    self.refrescar_lista()
                    self.vista.set_estado(f"Usuario '{usuario.nombre}' eliminado")
                except Exception as e:
                    self.vista.set_estado(f"Error al eliminar: {e}")
        else:
            self.vista.set_estado("No se pudo eliminar (índice inválido)")

    #Editar usuario
    def editar_usuario(self, indice):
        usuarios = self.modelo.listar()
        if 0 <= indice < len(usuarios):
            usuario = usuarios[indice]
            modal = AltaUsuarioModal(
                self.root,
                lambda n, e, g, a: self.confirmar_edicion(indice, n, e, g, a),
                self.avatars
            )
            # Pre-cargar datos del usuario en el modal
            modal.entry_nombre.insert(0, usuario.nombre)
            modal.entry_edad.insert(0, str(usuario.edad))
            modal.var_genero.set(usuario.genero)
            if usuario.avatar:
                modal.seleccionar_avatar(usuario.avatar)

            self.vista.set_estado(f"Editando a {usuario.nombre}...")
        else:
            self.vista.set_estado("No se pudo editar (índice inválido)")

    def confirmar_edicion(self, indice, nombre, edad, genero, avatar):
        try:
            actualizado = Usuario(nombre, edad, genero, avatar)
            self.modelo.actualizar(indice, actualizado)
            self.refrescar_lista()
            self.vista.set_estado(f"Usuario '{nombre}' actualizado correctamente")
        except Exception as e:
            self.vista.set_estado(f"Error al actualizar: {e}")

    # Buscar y Filtrar
    def buscar(self, texto=None, genero=None):
        try:
            if texto is None:
                texto = self.vista.entry_buscar.get()
            if genero is None:
                genero = self.vista.combo_genero.get()

            resultado = self.modelo.filtrar(texto, genero)
            self.vista.usuarios = resultado
            self.vista.lista.delete(0, "end")
            for i, u in enumerate(resultado):
                self.vista.lista.insert("end", f"{u.nombre} ({u.edad} años, {u.genero})")

            self.vista.set_estado(f"{len(resultado)} usuario(s) encontrados")
        except Exception as e:
            self.vista.set_estado(f"Error en la búsqueda: {e}")

    #Guardar y Cargar
    def guardar(self):
        try:
            self.modelo.guardar_csv()
            self.vista.set_estado("Usuarios guardados correctamente")
        except Exception as e:
            self.vista.set_estado(f"Error al guardar: {e}")

    def cargar(self, inicial=False):
        try:
            self.modelo.cargar_csv()
            self.refrescar_lista()
            if inicial:
                self.vista.set_estado("Aplicación lista")
            else:
                self.vista.set_estado("Usuarios cargados correctamente")
        except FileNotFoundError:
            self.vista.set_estado("No se encontró el archivo CSV (se creará al guardar)")
        except Exception as e:
            self.vista.set_estado(f"Error al cargar: {e}")

    #Salir
    def salir(self):
        # Detener el hilo de auto-guardado antes de salir
        self.detener_auto_guardado()

        try:
            self.guardar()
            self.vista.set_estado("Cambios guardados. Cerrando aplicación...")
        except Exception:
            self.vista.set_estado("Saliendo sin guardar por error inesperado")
        self.root.quit()