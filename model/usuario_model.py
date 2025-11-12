class Usuario:
    def __init__(self, nombre: str, edad: int, genero: str, avatar: str = None):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar  # ruta de imagen opcional

    def __str__(self):
        return f"{self.nombre} - {self.edad} años - {self.genero}"


class GestorUsuarios:
    def __init__(self):
        self._usuarios = []  # lista interna de objetos Usuario

    def listar(self):
        return list(self._usuarios)  # devolvemos copia

    def añadir(self, usuario: Usuario):
        if not usuario.nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not (0 <= usuario.edad <= 100):
            raise ValueError("La edad debe estar entre 0 y 100.")
        if usuario.genero.lower() not in ["masculino", "femenino", "otro"]:
            raise ValueError("Género inválido.")
        self._usuarios.append(usuario)

    def eliminar(self, indice: int):
        if 0 <= indice < len(self._usuarios):
            del self._usuarios[indice]
        else:
            raise IndexError("Índice fuera de rango.")

    def actualizar(self, indice: int, usuario_actualizado: Usuario):
        if 0 <= indice < len(self._usuarios):
            self._usuarios[indice] = usuario_actualizado
        else:
            raise IndexError("Índice fuera de rango.")
