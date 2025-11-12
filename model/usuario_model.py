import csv

class Usuario:
    def __init__(self, nombre: str, edad: int, genero: str, avatar: str = None):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar

    def __str__(self):
        return f"{self.nombre} - {self.edad} años - {self.genero}"


class GestorUsuarios:
    def __init__(self):
        self._usuarios = []

    def listar(self):
        return list(self._usuarios)

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

    # ---- Persistencia CSV ----
    def guardar_csv(self, ruta: str = "usuarios.csv"):
        try:
            with open(ruta, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["nombre", "edad", "genero", "avatar"])
                for u in self._usuarios:
                    writer.writerow([u.nombre, u.edad, u.genero, u.avatar])
        except Exception as e:
            raise IOError(f"Error al guardar CSV: {e}")

    def cargar_csv(self, ruta: str = "usuarios.csv"):
        self._usuarios.clear()
        try:
            with open(ruta, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    try:
                        nombre = fila["nombre"].strip()
                        edad = int(fila["edad"])
                        genero = fila["genero"]
                        avatar = fila.get("avatar", None)
                        self._usuarios.append(Usuario(nombre, edad, genero, avatar))
                    except Exception:
                        continue  # Ignora filas corruptas
        except FileNotFoundError:
            pass  # No existe el CSV aún
        except Exception as e:
            raise IOError(f"Error al cargar CSV: {e}")

    # ---- Búsqueda y filtrado ----
    def filtrar(self, texto_busqueda: str = "", genero: str = "Todos"):
        resultado = []
        texto_busqueda = texto_busqueda.lower().strip()

        for u in self._usuarios:
            coincide_nombre = texto_busqueda in u.nombre.lower()
            coincide_genero = (genero == "Todos") or (u.genero.lower() == genero.lower())

            if coincide_nombre and coincide_genero:
                resultado.append(u)

        return resultado
