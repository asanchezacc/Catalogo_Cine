from src import menu
from src.modelos import usuarios
from src.datos import datos_iniciales


def preparar_usuarios():
    """Carga los usuarios de prueba y guarda el estado original del modulo."""
    usuarios_originales = [usuario.copy() for usuario in usuarios.usuarios]
    historial_original = usuarios.HISTORIAL[:]
    datos_iniciales.cargar_usuarios()
    return usuarios_originales, historial_original


def restaurar_usuarios(usuarios_originales, historial_original):
    """Restaura los usuarios y el historial que habia antes del test."""
    usuarios.usuarios[:] = usuarios_originales
    usuarios.HISTORIAL[:] = historial_original


# ------------------ Login ------------------

def test_login_usuario_inexistente_devuelve_false():
    originales, historial = preparar_usuarios()
    try:
        exito, mensaje = usuarios.verificar_credenciales("noexiste", "1234")
        assert exito is False
        assert mensaje == "Usuario no encontrado."
    finally:
        restaurar_usuarios(originales, historial)


def test_login_contrasena_incorrecta_devuelve_false():
    originales, historial = preparar_usuarios()
    try:
        exito, mensaje = usuarios.verificar_credenciales("admin", "clave_mala")
        assert exito is False
        assert mensaje == "Contraseña incorrecta."
    finally:
        restaurar_usuarios(originales, historial)


def test_login_correcto_devuelve_true_y_rol():
    originales, historial = preparar_usuarios()
    try:
        exito, rol = usuarios.verificar_credenciales("admin", "admin123")
        assert exito is True
        assert rol == "administrador"
    finally:
        restaurar_usuarios(originales, historial)


def test_login_usuario_vacio_devuelve_false():
    originales, historial = preparar_usuarios()
    try:
        exito, mensaje = usuarios.verificar_credenciales("", "")
        assert exito is False
    finally:
        restaurar_usuarios(originales, historial)


# ------------------ Busquedas y peliculas ------------------

def test_tickets_de_pelicula_filtra_por_id():
    lista = [
        {"id": 1, "cliente_id": 1, "pelicula_id": 2, "asiento": (0, 0), "precio": 2000, "estado": "pendiente"},
        {"id": 2, "cliente_id": 2, "pelicula_id": 3, "asiento": (0, 1), "precio": 2200, "estado": "cobrado"},
        {"id": 3, "cliente_id": 3, "pelicula_id": 2, "asiento": (1, 0), "precio": 2000, "estado": "pendiente"},
    ]
    resultado = menu.tickets_de_pelicula(2, lista)
    assert len(resultado) == 2
    assert resultado[0]["id"] == 1
    assert resultado[1]["id"] == 3
    assert menu.tickets_de_pelicula(9, lista) == []


def test_proximo_id_pelicula():
    assert menu.proximo_id_pelicula([]) == 1
    assert menu.proximo_id_pelicula([{"id": 1}, {"id": 4}, {"id": 2}]) == 5
