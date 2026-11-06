
"""Pruebas de altas, bajas y cambios de contraseña en el archivo TXT."""

from src.modelos import usuarios
from src.datos import datos_iniciales


ARCHIVO_PRUEBA = "usuarios_pruebas_pytest.txt"


def preparar_prueba():

    """Usa un TXT exclusivo y guarda el estado anterior del módulo."""

    ruta_original = usuarios.ARCHIVO_USUARIOS
    lista_original = [usuario.copy() for usuario in usuarios.usuarios]
    historial_original = usuarios.HISTORIAL[:]
    usuarios.ARCHIVO_USUARIOS = ARCHIVO_PRUEBA
    usuarios.usuarios.clear()
    usuarios.HISTORIAL.clear()
    return ruta_original, lista_original, historial_original



def restaurar_prueba(ruta, lista, historial):

    """Restaura el módulo y borra únicamente el TXT de pruebas."""

    usuarios.ARCHIVO_USUARIOS = ruta
    usuarios.usuarios[:] = lista
    usuarios.HISTORIAL[:] = historial
    # El archivo de pruebas se reutiliza en la siguiente ejecución de pytest.



def test_usuarios_txt_alta_y_recuperacion():

    ruta, lista, historial = preparar_prueba()
    try:
        datos_iniciales.cargar_usuarios()
        assert usuarios.guardar_usuarios()[0] is True
        assert usuarios.alta_usuario("Ana Pérez", "ana", "Clave1!", "empleado")[0] is True
        usuarios.usuarios.clear()
        exito, existe, _ = usuarios.cargar_usuarios_desde_txt()
        assert exito is True and existe is True
        assert usuarios.buscar_usuario("ana")["nombre"] == "Ana Pérez"
        assert usuarios.verificar_credenciales("ana", "Clave1!")[0] is True
    finally:
        restaurar_prueba(ruta, lista, historial)



def test_usuarios_txt_cambio_contrasena_y_baja():

    ruta, lista, historial = preparar_prueba()
    try:
        datos_iniciales.cargar_usuarios()
        assert usuarios.guardar_usuarios()[0] is True
        assert usuarios.alta_usuario("Ana", "ana", "Clave1!", "empleado")[0] is True
        assert usuarios.actualizar_contrasena("ana", "Nueva2!")[0] is True
        usuarios.usuarios.clear()
        assert usuarios.cargar_usuarios_desde_txt()[0] is True
        assert usuarios.verificar_credenciales("ana", "Nueva2!")[0] is True
        assert usuarios.baja_usuario("ana")[0] is True
        usuarios.usuarios.clear()
        assert usuarios.cargar_usuarios_desde_txt()[0] is True
        assert usuarios.buscar_usuario("ana") is None
    finally:
        restaurar_prueba(ruta, lista, historial)



def test_usuarios_txt_danado_no_modifica_memoria():

    ruta, lista, historial = preparar_prueba()
    try:
        datos_iniciales.cargar_usuarios()
        with open(ARCHIVO_PRUEBA, "w", encoding="utf-8") as archivo:
            archivo.write("contenido incorrecto sin separadores\n")
        exito, existe, _ = usuarios.cargar_usuarios_desde_txt()
        assert exito is False and existe is True
        assert usuarios.buscar_usuario("admin") is not None
    finally:
        restaurar_prueba(ruta, lista, historial)



def test_usuarios_txt_falla_guardado_y_no_aplica_alta():

    ruta, lista, historial = preparar_prueba()
    try:
        datos_iniciales.cargar_usuarios()
        usuarios.ARCHIVO_USUARIOS = "src/datos/carpeta_inexistente/usuarios.txt"
        exito, _ = usuarios.alta_usuario("Ana", "ana", "Clave1!", "empleado")
        assert exito is False
        assert usuarios.buscar_usuario("ana") is None
    finally:
        restaurar_prueba(ruta, lista, historial)


def test_usuario_duplicado_con_mayusculas():
    ruta, lista, historial = preparar_prueba()
    try:
        datos_iniciales.cargar_usuarios()
        exito, _ = usuarios.alta_usuario("Otro admin", "ADMIN", "Clave1!", "empleado", persistir=False)
        assert exito is False
        assert len(usuarios.usuarios) == len(datos_iniciales.USUARIOS_INICIALES)
        assert usuarios.verificar_credenciales("ADMIN", "admin123")[0] is True
    finally:
        restaurar_prueba(ruta, lista, historial)


def test_archivo_usuarios_rechaza_nombres_repetidos_con_mayusculas():
    ruta, lista, historial = preparar_prueba()
    try:
        datos_iniciales.cargar_usuarios()
        with open(ARCHIVO_PRUEBA, "w", encoding="utf-8") as archivo:
            archivo.write("1;Admin;admin;admin123;administrador\n")
            archivo.write("2;Otro;ADMIN;Clave1!;empleado\n")
        exito, existe, _ = usuarios.cargar_usuarios_desde_txt()
        assert exito is False and existe is True
        assert len(usuarios.usuarios) == len(datos_iniciales.USUARIOS_INICIALES)
    finally:
        restaurar_prueba(ruta, lista, historial)
