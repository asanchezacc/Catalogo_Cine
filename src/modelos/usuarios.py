import json

ARCHIVO_USUARIOS = "src/datos/usuarios.json"

usuarios = []
HISTORIAL = []


def _proximo_id(lista_usuarios):
    if not lista_usuarios:
        return 1
    ids = [usuario["id"] for usuario in lista_usuarios]
    return max(ids) + 1


def buscar_usuario(usuario):
    """Busca un usuario por su nombre de usuario."""
    for dato in usuarios:
        if dato["usuario"] == usuario:
            return dato
    return None


def verificar_credenciales(usuario, contrasena):
    """Verifica las credenciales y devuelve el rol si son correctas."""
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."

    if datos["contraseña"] != contrasena:
        return False, "Contraseña incorrecta."

    return True, datos["rol"]


def alta_usuario(nombre, usuario, contrasena, rol):
    """Agrega un usuario si el nombre de usuario no existe y lo guarda en JSON."""
    if not nombre.strip():
        return False, "El nombre no puede estar vacío."

    if buscar_usuario(usuario) is not None:
        return False, "Ese nombre de usuario ya existe."

    nuevo_usuario = {
        "id": _proximo_id(usuarios),
        "nombre": nombre.strip(),
        "usuario": usuario,
        "contraseña": contrasena,
        "rol": rol,
    }

    usuarios.append(nuevo_usuario)

    guardado, mensaje = guardar_usuarios()
    if not guardado:
        usuarios.pop()
        return False, mensaje

    HISTORIAL.append(("alta", usuario, rol))
    return True, nuevo_usuario


def baja_usuario(usuario):
    """Elimina un usuario por su nombre de usuario y guarda el cambio en JSON."""
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."

    posicion = usuarios.index(datos)
    usuarios.remove(datos)

    guardado, mensaje = guardar_usuarios()
    if not guardado:
        usuarios.insert(posicion, datos)
        return False, mensaje

    HISTORIAL.append(("baja", usuario, datos["rol"]))
    return True, f"Usuario '{usuario}' eliminado."


def actualizar_contrasena(usuario, nueva_contrasena):
    """Actualiza la contraseña de un usuario y guarda el cambio en JSON."""
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."

    contrasena_anterior = datos["contraseña"]
    datos["contraseña"] = nueva_contrasena

    guardado, mensaje = guardar_usuarios()
    if not guardado:
        datos["contraseña"] = contrasena_anterior
        return False, mensaje

    HISTORIAL.append(("actualizacion", usuario, datos["rol"]))
    return True, "Contraseña actualizada correctamente."


def ver_historial(accion=None):
    """Devuelve el historial completo o solo una acción."""
    if accion is None:
        return HISTORIAL
    return [entrada for entrada in HISTORIAL if entrada[0] == accion]


def iniciar_sesion(intentos_maximos=3):
    """Solicita credenciales y devuelve el usuario y su rol."""
    intento = 0

    while intento < intentos_maximos:
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ")

        exito, resultado = verificar_credenciales(usuario, contrasena)

        if exito:
            print(f"¡Bienvenido/a, {usuario}! Rol: {resultado}")
            return usuario, resultado

        intento += 1
        intentos_restantes = intentos_maximos - intento
        print(f"{resultado} Te quedan {intentos_restantes} intento(s).")

    print("Se agotaron los intentos. Cerrando sesión.")
    return None, None

    
def guardar_usuarios():
    """Guarda la lista de usuarios en el archivo JSON. Devuelve (exito, mensaje)."""
    try:
        with open(ARCHIVO_USUARIOS, "w", encoding="UTF-8") as archivo:
            # ensure_ascii=False para que guarde tildes y ñ correctamente
            json.dump(usuarios, archivo, ensure_ascii=False, indent=4)
    except OSError as error:
        return False, f"No se pudieron guardar los usuarios: {error}"

    return True, "Usuarios guardados correctamente."


def cargar_usuarios_desde_json():
    """Carga los usuarios guardados en el JSON. Devuelve (exito, mensaje)."""
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="UTF-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return True, "Todavía no existe un archivo de usuarios."
    except (OSError, json.JSONDecodeError) as error:
        return False, f"No se pudieron cargar los usuarios: {error}"

    # Se modifica la lista en el lugar para no perder la referencia de otros módulos
    usuarios[:] = datos
    return True, f"Se cargaron {len(datos)} usuarios."