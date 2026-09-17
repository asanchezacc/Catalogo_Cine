usuarios = []

HISTORIAL = []


def _proximo_id(lista_usuarios):
    if not lista_usuarios:
        return 1
    ids = [u["id"] for u in lista_usuarios]
    return max(ids) + 1


def buscar_usuario(usuario):
    for u in usuarios:
        if u["usuario"] == usuario:
            return u
    return None


def verificar_credenciales(usuario, contrasena):
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."

    if datos["contraseña"] != contrasena:
        return False, "Contraseña incorrecta."

    return True, datos["rol"]


def alta_usuario(nombre, usuario, contrasena, rol, mostrar_mensajes=True):
    if not nombre.strip():
        if mostrar_mensajes:
            print("El nombre no puede estar vacío.")
        return False, "El nombre no puede estar vacío."

    if buscar_usuario(usuario) is not None:
        if mostrar_mensajes:
            print("Ese nombre de usuario ya existe.")
        return False, "Ese nombre de usuario ya existe."

    nuevo_usuario = {
        "id": _proximo_id(usuarios),
        "nombre": nombre.strip(),
        "usuario": usuario,
        "contraseña": contrasena,
        "rol": rol,
    }

    usuarios.append(nuevo_usuario)
    HISTORIAL.append(("alta", usuario, rol))
    if mostrar_mensajes:
        print(f"Usuario '{usuario}' dado de alta.")
    return True, nuevo_usuario


def baja_usuario(usuario):
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."

    usuarios.remove(datos)
    HISTORIAL.append(("baja", usuario, datos["rol"]))
    return True, f"Usuario '{usuario}' eliminado."


def actualizar_contrasena(usuario, nueva_contrasena):
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."

    datos["contraseña"] = nueva_contrasena
    HISTORIAL.append(("actualizacion", usuario, datos["rol"]))
    return True, "Contraseña actualizada correctamente."


def ver_historial(accion=None):
    if accion is None:
        return HISTORIAL
    return [entrada for entrada in HISTORIAL if entrada[0] == accion]


def iniciar_sesion(intentos_maximos=3):
    intento = 0

    while intento < intentos_maximos:
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ")

        exito, resultado = verificar_credenciales(usuario, contrasena)

        if exito:
            rol = resultado
            print(f"¡Bienvenido/a, {usuario}! Rol: {rol}")
            return usuario, rol

        intento += 1
        intentos_restantes = intentos_maximos - intento
        print(f"{resultado} Te quedan {intentos_restantes} intento(s).")

    print("Se agotaron los intentos. Cerrando sesión.")
    return None, None

