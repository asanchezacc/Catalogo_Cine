"""
Módulo de vista
Funciones para imprimir mensajes con color y mostrar tablas de datos
(peliculas, clientes, empleados, tickets, etc.) en pantalla.
"""

# CONFIGURACION DE COLORES ANSI
RESET = "\033[0m" # resetea todo el formato
BOLD = "\033[1m" # texto en negrita
ROJO = "\033[31;1m"
VERDE = "\033[32;1m"
AMARILLO = "\033[33;1m"
AZUL = "\033[34;1m"
MAGENTA = "\033[35;1m"
CYAN = "\033[36;1m"
BLANCO = "\033[37;1m"

# FUNCIONES PARA IMPRIMIR MENSAJES
def imprimir_mensaje(texto, color=BLANCO):
    # mensaje con el color especificado
    print(f"{color}{texto}{RESET}")

def imprimir_encabezado(texto):
    # se aplica metodos de cadena: .upper() (mayusculas) y .center() (centado)
    texto_formateado = texto.upper()
    print(f"\n{AZUL}{BOLD}{'=' * 50}{RESET}")
    print(f"{AZUL}{BOLD}{texto_formateado.center(50)}{RESET}")
    print(f"{AZUL}{BOLD}{'=' * 50}{RESET}\n")

def imprimir_error(texto):
    # errores en rojo
    imprimir_mensaje(f"ERROR: {texto}", ROJO)

def imprimir_exito(texto):
    # exitos en verde
    imprimir_mensaje(f"EXITO: {texto}", VERDE)

def imprimir_advertencia(texto):
    # advertencias en amarillo
    imprimir_mensaje(f"ADVERTENCIA: {texto}", AMARILLO)

# FUNCIONES LAMBDA PARA DAR FORMATO A VALORES
formatear_precio = lambda p: f"${p:.2f}"
formatear_estado = lambda activo: "Activo" if activo else "Inactivo"
formatear_disponibilidad = lambda disponible: "Si" if disponible else "No"

# FUNCION PARA MOSTRAR CUALQUIER TABLA DE DATOS
def mostrar_tabla(datos, columnas, con_encabezado=True):
    """
    Muestra en pantalla una lista de diccionarios como una tabla
    """
    if not datos:
        imprimir_advertencia("La lista esta vacia. No hay nada que mostrar.")
        return

    if con_encabezado:
        print(f"{CYAN}{BOLD}", end="")
        for etiqueta, clave, ancho in columnas:
            print(f"{etiqueta.upper():<{ancho}}", end=" ")
        print()
        print(f"{'-' * 60}{RESET}")

    for fila in datos:
        for etiqueta, clave, ancho in columnas:
            valor = fila.get(clave, "")
            print(f"{valor:<{ancho}}", end=" ")
        print()

# FUNCION PARA MOSTRAR EL CATALOGO DE PELICULAS
def mostrar_catalogo(peliculas, con_encabezado=True):
    columnas = [
        ("ID", "id", 4),
        ("Titulo", "titulo", 25),
        ("Genero", "genero", 15),
        ("Duracion", "duracion", 10),
        ("Precio", "precio", 10),
    ]
    mostrar_tabla(peliculas, columnas, con_encabezado)

# FUNCION PARA MOSTRAR UNA MATRIZ
def mostrar_matriz(matriz, encabezados=None, ancho=20):
    """Muestra en pantalla una matriz con formato de tabla."""
    if not matriz:
        imprimir_advertencia("La matriz está vacía. No hay nada que mostrar.")
        return

    if encabezados:
        print(f"{CYAN}{BOLD}", end="")
        for titulo in encabezados:
            print(f"{titulo.upper():<{ancho}}", end="")
        print()
        print(f"{CYAN}{'-' * (len(encabezados) * ancho)}{RESET}")

    # Mostrar filas
    for fila in matriz:
        for valor in fila:
            if type(valor) == bool:
                if valor:
                    valor = "Activo"
                else:
                    valor = "Inactivo"
            print(f"{str(valor):<{ancho}}", end="")
        print()

# BLOQUE DE EJECUCION
if __name__ == "__main__":
    peliculas = [
        {"id": 1, "titulo": "Spiderman Brand New Day", "genero": "Accion", "duracion": 150, "precio": 2500},
        {"id": 2, "titulo": "La Odisea", "genero": "Drama", "duracion": 90, "precio": 2000},
        {"id": 3, "titulo": "Supergirl", "genero": "Ciencia ficcion", "duracion": 120, "precio": 2200},
        {"id": 4, "titulo": "Mortal Kombat II", "genero": "Accion", "duracion": 100, "precio": 2400},
        {"id": 5, "titulo": "Maestros del Universo", "genero": "Aventura", "duracion": 110, "precio": 2300},
    ]

    # Probando el encabezado
    imprimir_encabezado("El archivo de vista funciona")

    # Mensajes de colores
    imprimir_exito("Conexion establecida")
    imprimir_error("Archivo no encontrado")
    imprimir_advertencia("Quedan pocos intentos")

    # Impresion de la tabla
    print("\n--- MOSTRANDO CATALOGO DE PELICULAS ---")
    mostrar_catalogo(peliculas)

    # Lista de clientes
    clientes = [
        {"id": 1, "nombre": "Lary Choi", "email": "larychoi@mail.com", "telefono": "1122334455", "estado": True},
        {"id": 2, "nombre": "Tómas Moran", "email": "tomasmoran@mail.com", "telefono": "1166778899", "estado": False},
    ]
    columnas_clientes = [
        ("ID", "id", 4),
        ("Nombre", "nombre", 20),
        ("Email", "email", 25),
        ("Telefono", "telefono", 15),
    ]
    print("\n--- MOSTRANDO CLIENTES ---")
    mostrar_tabla(clientes, columnas_clientes)

    print("\n--- MOSTRANDO MATRIZ DE EMPLEADOS ---")
    empleados = [
        [1, "Alan Yerusalmi", "alan@email.com", True],
        [2, "Julieta Spam", "julieta@email.com", False],
    ]

    encabezados_emp = ["ID", "Nombre", "Email", "Estado"]
    mostrar_matriz(empleados, encabezados_emp)
