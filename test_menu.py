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


# ------------------ Grilla de la sala ------------------

def test_armar_grilla_sala_marca_ocupados():
    mapa = {(0, 0): "Libre", (0, 1): "Ocupado", (1, 0): "Libre", (1, 1): "Libre"}
    lineas = menu.armar_grilla_sala(mapa, 2, 2)
    assert len(lineas) == 3
    assert lineas[0] == "        0  1"
    assert lineas[1] == "Fila 0  -  X"
    assert lineas[2] == "Fila 1  -  -"


# ------------------ Estadisticas ------------------

def test_titulos_de_ids():
    lista = [{"id": 1, "titulo": "A"}, {"id": 2, "titulo": "B"}, {"id": 3, "titulo": "C"}]
    assert menu.titulos_de_ids({1, 3}, lista) == ["A", "C"]
    assert menu.titulos_de_ids(set(), lista) == []


def test_tickets_activos_de_pelicula_ignora_cancelados():
    lista = [
        {"id": 1, "pelicula_id": 2, "estado": "pendiente"},
        {"id": 2, "pelicula_id": 2, "estado": "cancelado"},
        {"id": 3, "pelicula_id": 2, "estado": "cobrado"},
        {"id": 4, "pelicula_id": 5, "estado": "pendiente"},
    ]
    activos = menu.tickets_activos_de_pelicula(2, lista)
    assert len(activos) == 2
    assert activos[0]["id"] == 1
    assert activos[1]["id"] == 3
    assert menu.tickets_activos_de_pelicula(9, lista) == []


def test_titulo_repetido_sin_importar_mayusculas():
    lista = [{"id": 1, "titulo": "Supergirl"}, {"id": 2, "titulo": "La Odisea"}]
    assert menu.titulo_repetido("supergirl", lista) is True
    assert menu.titulo_repetido("Avatar 3", lista) is False
    # Al modificar la película 1 puede conservar su propio título
    assert menu.titulo_repetido("Supergirl", lista, 1) is False
    assert menu.titulo_repetido("La Odisea", lista, 1) is True


def test_linea_ticket_muestra_nombre_y_titulo():
    menu.PELICULAS.append({"id": 900, "titulo": "Pelicula de prueba", "genero": "Drama", "duracion": 90, "precio": 2000})
    try:
        ticket = {"id": 1, "cliente_id": 9999, "pelicula_id": 900, "asiento": (2, 3), "precio": 2000, "estado": "pendiente"}
        linea = menu.linea_ticket(ticket)
        assert "Pelicula de prueba" in linea
        assert "fila 2 col 3" in linea
        assert "2000.00" in linea
        # El cliente 9999 no existe, por eso aparece "?"
        assert "?" in linea
    finally:
        menu.PELICULAS.pop()


# ------------------ Ordenar clientes ------------------

def test_clientes_para_tabla_no_modifica_originales():
    lista = [{"id": 1, "nombre": "A", "estado": True}, {"id": 2, "nombre": "B", "estado": False}]
    tabla = menu.clientes_para_tabla(lista)
    assert tabla[0]["estado"] == "Activo"
    assert tabla[1]["estado"] == "Inactivo"
    # Las originales siguen con True/False
    assert lista[0]["estado"] is True
    assert lista[1]["estado"] is False
