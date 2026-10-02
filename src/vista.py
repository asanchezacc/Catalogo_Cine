"""
Módulo de vista
Funciones para imprimir mensajes con color y mostrar tablas de datos
(peliculas, clientes, empleados, tickets, etc.) en pantalla.
"""

# CONFIGURACION DE COLORES ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
ROJO = "\033[31;1m"
VERDE = "\033[32;1m"
AMARILLO = "\033[33;1m"
AZUL = "\033[34;1m"
MAGENTA = "\033[35;1m"
CYAN = "\033[36;1m"
BLANCO = "\033[37;1m"


def imprimir_mensaje(texto, color=BLANCO):
    """Imprime un mensaje con el color especificado."""
    print(f"{color}{texto}{RESET}")


def imprimir_encabezado(texto):
    """Imprime un encabezado con separadores y color."""
    texto_formateado = texto.upper()
    print(f"\n{AZUL}{BOLD}{'=' * 50}{RESET}")
    print(f"{AZUL}{BOLD}{texto_formateado.center(50)}{RESET}")
    print(f"{AZUL}{BOLD}{'=' * 50}{RESET}\n")


def imprimir_error(texto):
    imprimir_mensaje(f"ERROR: {texto}", ROJO)


def imprimir_exito(texto):
    imprimir_mensaje(f"EXITO: {texto}", VERDE)


def imprimir_advertencia(texto):
    imprimir_mensaje(f"ADVERTENCIA: {texto}", AMARILLO)


# FUNCIONES LAMBDA PARA DAR FORMATO A VALORES
formatear_precio = lambda p: f"${p:.2f}"
formatear_estado = lambda activo: "Activo" if activo else "Inactivo"
formatear_disponibilidad = lambda disponible: "Si" if disponible else "No"


def mostrar_tabla(datos, columnas, con_encabezado=True):
    """Muestra en pantalla una lista de diccionarios como una tabla."""
    if not datos:
        imprimir_advertencia("La lista esta vacia. No hay nada que mostrar.")
        return

    if con_encabezado:
        print(f"{CYAN}{BOLD}", end="")
        for etiqueta, clave, ancho in columnas:
            print(f"{etiqueta.upper():<{ancho}}", end=" ")
        print()

        # Linea separadora de ancho dinamico segun las columnas
        ancho_total = sum(ancho + 1 for _, _, ancho in columnas)
        print(f"{'-' * ancho_total}{RESET}")

    for fila in datos:
        for etiqueta, clave, ancho in columnas:
            valor = str(fila.get(clave, ""))

            # Slicing para no romper la tabla si el valor es muy largo
            if len(valor) > ancho:
                valor = valor[:ancho - 1] + "…"

            print(f"{valor:<{ancho}}", end=" ")
        print()


def mostrar_catalogo(peliculas, con_encabezado=True):
    columnas = [
        ("ID", "id", 4),
        ("Titulo", "titulo", 25),
        ("Genero", "genero", 15),
        ("Duracion", "duracion", 10),
        ("Precio", "precio", 10),
    ]
    mostrar_tabla(peliculas, columnas, con_encabezado)


def mostrar_matriz(matriz, encabezados=None, anchos=None, ancho=20):
    """Muestra una matriz con formato de tabla."""
    if not matriz:
        imprimir_advertencia("La matriz está vacía. No hay nada que mostrar.")
        return

    columnas = len(matriz[0]) if matriz else 0

    if anchos is None:
        anchos = [ancho] * columnas

    if encabezados:
        print(f"{CYAN}{BOLD}", end="")
        for i, titulo in enumerate(encabezados):
            print(f"{titulo.upper():<{anchos[i]}}", end="")
        print()
        print(f"{CYAN}{'-' * sum(anchos)}{RESET}")

    for fila in matriz:
        for i, valor in enumerate(fila):
            if type(valor) == bool:
                valor = "Activo" if valor else "Inactivo"

            texto = str(valor)

            if len(texto) > anchos[i]:
                texto = texto[:anchos[i] - 1] + "."

            print(f"{texto:<{anchos[i]}}", end="")
        print()


def mostrar_sala(sala, titulo="SALA"):
    """
    Muestra la sala como una grilla visual, similar a las plataformas reales de venta de entradas:
      - Letras a la izquierda para las filas.
      - Numeros arriba para las columnas.
      - '·' verde para asiento libre, 'X' rojo para ocupado.
    """
    if not sala or not sala[0]:
        imprimir_advertencia("La sala está vacía.")
        return

    filas = len(sala)
    columnas = len(sala[0])
    ancho_total = 5 + columnas * 3

    imprimir_encabezado(titulo)
    print(f"{CYAN}{BOLD}{'PANTALLA'.center(ancho_total)}{RESET}")
    print(f"{CYAN}{'-' * ancho_total}{RESET}")

    # Numeros de columna
    print(f"{CYAN}{BOLD}{'':5}{RESET}", end="")
    for j in range(columnas):
        print(f"{CYAN}{BOLD}{j + 1:>3}{RESET}", end="")
    print()

    # Filas con letras
    for i, fila in enumerate(sala):
        letra = chr(ord('A') + i)
        print(f"{CYAN}{BOLD}{letra:<5}{RESET}", end="")
        for valor in fila:
            if valor == 0:
                print(f"{VERDE}  ·{RESET}", end="")
            else:
                print(f"{ROJO}  X{RESET}", end="")
        print()

    print()
    print(f"  {VERDE}·{RESET} Libre    {ROJO}X{RESET} Ocupado")


def mostrar_sala_con_tickets(sala, tickets, titulo="SALA - OCUPACION"):
    """Igual que mostrar_sala, pero marca cada asiento ocupado con el IDdel cliente que hizo la reserva."""
    if not sala or not sala[0]:
        imprimir_advertencia("La sala está vacía.")
        return

    # Mapa {(fila, columna): cliente_id}
    reservados = {}
    for t in tickets:
        if t["estado"] in ("pendiente", "cobrado"):
            reservados[t["asiento"]] = t["cliente_id"]

    columnas = len(sala[0])
    ancho_total = 5 + columnas * 3

    imprimir_encabezado(titulo)
    print(f"{CYAN}{BOLD}{'PANTALLA'.center(ancho_total)}{RESET}")
    print(f"{CYAN}{'-' * ancho_total}{RESET}")

    print(f"{CYAN}{BOLD}{'':5}{RESET}", end="")
    for j in range(columnas):
        print(f"{CYAN}{BOLD}{j + 1:>3}{RESET}", end="")
    print()

    for i, fila in enumerate(sala):
        letra = chr(ord('A') + i)
        print(f"{CYAN}{BOLD}{letra:<5}{RESET}", end="")
        for j, valor in enumerate(fila):
            coord = (i, j)
            if valor == 0:
                print(f"{VERDE}  ·{RESET}", end="")
            elif coord in reservados:
                cliente_id = reservados[coord]
                print(f"{AMARILLO}{cliente_id:>3}{RESET}", end="")
            else:
                print(f"{ROJO}  X{RESET}", end="")
        print()

    print()
    print(f"    {VERDE}·{RESET} Libre   {ROJO}X{RESET}  Ocupado  {AMARILLO}N{RESET} Cliente N")


# BLOQUE DE EJECUCION
if __name__ == "__main__":
    peliculas = [
        {"id": 1, "titulo": "Spiderman Brand New Day", "genero": "Accion", "duracion": 150, "precio": 2500},
        {"id": 2, "titulo": "La Odisea", "genero": "Drama", "duracion": 90, "precio": 2000},
        {"id": 3, "titulo": "Supergirl", "genero": "Ciencia ficcion", "duracion": 120, "precio": 2200},
        {"id": 4, "titulo": "Mortal Kombat II", "genero": "Accion", "duracion": 100, "precio": 2400},
        {"id": 5, "titulo": "Maestros del Universo", "genero": "Aventura", "duracion": 110, "precio": 2300},
    ]

    imprimir_encabezado("El archivo de vista funciona")
    imprimir_exito("Conexion establecida")
    imprimir_error("Archivo no encontrado")
    imprimir_advertencia("Quedan pocos intentos")

    print("\n--- MOSTRANDO CATALOGO DE PELICULAS ---")
    mostrar_catalogo(peliculas)

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
    anchos_emp = [5, 20, 30, 12]
    mostrar_matriz(empleados, encabezados_emp, anchos_emp)

    print("\n--- MOSTRANDO SALA DE CINE ---")
    sala = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    mostrar_sala(sala)
