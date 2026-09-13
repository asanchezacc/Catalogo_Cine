ROLES_ASIGNABLES = {"empleado"}

PERMISOS_BORRAR = [
    ("admin", "empleado"),
]

HISTORIAL = []


def buscar_usuario(usuario, usuarios):
    for u in usuarios:
        if u["usuario"] == usuario:
            return u
    return None


def verificar_credenciales(usuario, contrasena, usuarios):
    datos = buscar_usuario(usuario, usuarios)

    if datos is None:
        return False, "Usuario no encontrado."

    if datos["contraseña"] != contrasena:
        return False, "Contraseña incorrecta."

    return True, datos["rol"]


def agregar_usuario(usuario_que_agrega, nuevo_usuario, contrasena, rol, usuarios):
    quien = buscar_usuario(usuario_que_agrega, usuarios)

    if quien is None:
        return False, "El usuario que intenta agregar no existe."

    if quien["rol"] != "admin":
        return False, "No tenés permiso para agregar usuarios."

    if rol not in ROLES_ASIGNABLES:
        return False, "El rol debe ser 'empleado'."

    if buscar_usuario(nuevo_usuario, usuarios) is not None:
        return False, "Ese nombre de usuario ya existe."

    usuarios.append({"usuario": nuevo_usuario, "contraseña": contrasena, "rol": rol})
    HISTORIAL.append(("alta", nuevo_usuario, rol))
    return True, f"Usuario '{nuevo_usuario}' agregado como {rol}."


def eliminar_usuario(usuario_que_borra, usuario_a_borrar, usuarios):
    quien = buscar_usuario(usuario_que_borra, usuarios)
    objetivo = buscar_usuario(usuario_a_borrar, usuarios)

    if quien is None:
        return False, "El usuario que intenta borrar no existe."

    if objetivo is None:
        return False, "El usuario a borrar no existe."

    rol_quien = quien["rol"]
    rol_objetivo = objetivo["rol"]
    dupla = (rol_quien, rol_objetivo)
    se_da_de_baja_a_si_mismo = rol_quien == "empleado" and usuario_que_borra == usuario_a_borrar

    if dupla not in PERMISOS_BORRAR and not se_da_de_baja_a_si_mismo:
        return False, f"Un {rol_quien} no tiene permiso para borrar a un {rol_objetivo}."

    usuarios.remove(objetivo)
    HISTORIAL.append(("baja", usuario_a_borrar, rol_objetivo))
    return True, f"Usuario '{usuario_a_borrar}' eliminado correctamente."


def actualizar_usuario(usuario_que_actualiza, usuario_a_actualizar, nueva_contrasena, usuarios):
    quien = buscar_usuario(usuario_que_actualiza, usuarios)
    objetivo = buscar_usuario(usuario_a_actualizar, usuarios)

    if quien is None or objetivo is None:
        return False, "Usuario inexistente."

    es_uno_mismo = usuario_que_actualiza == usuario_a_actualizar

    if not es_uno_mismo and quien["rol"] != "admin":
        return False, "No tenés permiso para modificar ese usuario."

    objetivo["contraseña"] = nueva_contrasena
    HISTORIAL.append(("actualizacion", usuario_a_actualizar, objetivo["rol"]))
    return True, "Contraseña actualizada correctamente."


def ver_historial(accion=None):
    if accion is None:
        return HISTORIAL
    return [entrada for entrada in HISTORIAL if entrada[0] == accion]


def iniciar_sesion(usuarios, intentos_maximos=3):
    intento = 0

    while intento < intentos_maximos:
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ")

        exito, resultado = verificar_credenciales(usuario, contrasena, usuarios)

        if exito:
            rol = resultado
            print(f"¡Bienvenido/a, {usuario}! Rol: {rol}")
            return usuario, rol

        intento += 1
        intentos_restantes = intentos_maximos - intento
        print(f"{resultado} Te quedan {intentos_restantes} intento(s).")

    print("Se agotaron los intentos. Cerrando sesión.")
    return None, None
