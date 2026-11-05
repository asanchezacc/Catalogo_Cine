"""Gestión de usuarios y persistencia en un archivo de texto."""

usuarios = []
HISTORIAL = []
ARCHIVO_USUARIOS = "src/datos/usuarios.txt"


def _proximo_id(lista_usuarios):
    if not lista_usuarios:
        return 1
    ids = [usuario["id"] for usuario in lista_usuarios]
    return max(ids) + 1


def _texto_valido(texto):
    """Comprueba que un campo pueda guardarse separado por punto y coma."""
    return (type(texto) == str and len(texto.strip()) > 0
            and ";" not in texto and "\n" not in texto and "\r" not in texto)


def guardar_usuarios():
    """Escribe todos los usuarios en un archivo TXT separado por punto y coma."""
    try:
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
            for dato in usuarios:
                linea = (f"{dato['id']};{dato['nombre']};{dato['usuario']};"
                         f"{dato['contraseña']};{dato['rol']}\n")
                archivo.write(linea)
        return True, "Usuarios guardados correctamente."
    except OSError as error:
        return False, f"No se pudieron guardar los usuarios: {error}"


def cargar_usuarios_desde_txt():
    """Lee los usuarios de TXT y no cambia la lista si el archivo es inválido.

    Devuelve (éxito, existe_archivo, mensaje).
    """
    cargados = []
    ids = set()
    nombres_usuario = set()

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            numero_linea = 0
            for linea in archivo:
                numero_linea += 1
                partes = linea.rstrip("\r\n").split(";")
                if len(partes) != 5:
                    raise ValueError(f"Formato incorrecto en línea {numero_linea}.")

                id_texto, nombre, usuario, contrasena, rol = partes
                id_usuario = int(id_texto)

                usuario_normalizado = usuario.strip().lower()
                if id_usuario <= 0 or id_usuario in ids or usuario_normalizado in nombres_usuario:
                    raise ValueError(f"ID o usuario repetido en línea {numero_linea}.")
                if (not _texto_valido(nombre) or not _texto_valido(usuario)
                        or not _texto_valido(contrasena)):
                    raise ValueError(f"Campo inválido en línea {numero_linea}.")
                if rol not in ("administrador", "empleado"):
                    raise ValueError(f"Rol inválido en línea {numero_linea}.")

                cargados.append({
                    "id": id_usuario,
                    "nombre": nombre,
                    "usuario": usuario,
                    "contraseña": contrasena,
                    "rol": rol,
                })
                ids.add(id_usuario)
                nombres_usuario.add(usuario_normalizado)

        if not cargados:
            raise ValueError("El archivo de usuarios está vacío.")

    except FileNotFoundError:
        return True, False, "Todavía no existe el archivo de usuarios."
    except (OSError, ValueError, UnicodeError) as error:
        return False, True, f"No se pudieron cargar los usuarios: {error}"

    usuarios[:] = cargados
    return True, True, f"Se cargaron {len(cargados)} usuarios del TXT."


def buscar_usuario(usuario):
    """Busca un usuario sin distinguir mayúsculas y minúsculas."""
    if type(usuario) != str:
        return None
    buscado = usuario.strip().lower()
    for dato in usuarios:
        if dato["usuario"].strip().lower() == buscado:
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


def alta_usuario(nombre, usuario, contrasena, rol, persistir=True):
    """Da de alta un usuario y guarda el cambio, salvo en la carga inicial."""
    if not _texto_valido(nombre):
        return False, "El nombre está vacío o contiene caracteres no permitidos."
    if not _texto_valido(usuario):
        return False, "El usuario está vacío o contiene caracteres no permitidos."
    if not _texto_valido(contrasena):
        return False, "La contraseña está vacía o contiene caracteres no permitidos."
    if rol not in ("administrador", "empleado"):
        return False, "El rol no es válido."

    usuario = usuario.strip()
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
    if persistir:
        exito, mensaje = guardar_usuarios()
        if not exito:
            usuarios.pop()
            return False, mensaje

    HISTORIAL.append(("alta", usuario, rol))
    return True, nuevo_usuario


def baja_usuario(usuario):
    """Borra un usuario y restaura la lista si falla el guardado."""
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."

    posicion = usuarios.index(datos)
    usuarios.pop(posicion)
    exito, mensaje = guardar_usuarios()
    if not exito:
        usuarios.insert(posicion, datos)
        return False, mensaje

    HISTORIAL.append(("baja", usuario, datos["rol"]))
    return True, f"Usuario '{usuario}' eliminado."


def actualizar_contrasena(usuario, nueva_contrasena):
    """Actualiza la contraseña y revierte el cambio si no pudo guardarse."""
    datos = buscar_usuario(usuario)

    if datos is None:
        return False, "Usuario no encontrado."
    if not _texto_valido(nueva_contrasena):
        return False, "La contraseña está vacía o contiene caracteres no permitidos."

    anterior = datos["contraseña"]
    datos["contraseña"] = nueva_contrasena
    exito, mensaje = guardar_usuarios()
    if not exito:
        datos["contraseña"] = anterior
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
