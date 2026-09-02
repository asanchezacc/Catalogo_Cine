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

# FUNCION PRINCIPAL: MOSTRAR CATALOGO EN TABLA
def mostrar_catalogo(catalogo, con_encabezado=True):
    if not catalogo:
        imprimir_advertencia("El catalogo esta vacio. No hay nada que mostrar.")
        return

    columnas_base = ["ID", "Titulo", "Genero", "Duracion"]
    encabezados = [col.upper() for col in columnas_base]

    if con_encabezado:
        print(f"{CYAN}{BOLD}", end="") # se activa los colores cyan y negrita

        # imprimimoos los encabezados usando f-strings y alineacion
        print(f"{encabezados[0]:<4} {encabezados[1]:<25} {encabezados[2]:<15}{encabezados[3]:<10}")

        # imprimimos la matriz
        print(f"{'-' * 60}{RESET}") # se resetea el color al terminar la linea

    # recorremos la matriz
    for pelicula in catalogo:
        # pelicula es una lista: [id, titulo, genero, duracion]
        print(f"{pelicula[0]:<4} {pelicula[1]:<25} {pelicula[2]:<15} {pelicula[3]:<10}")

# BLOQUE DE EJECUCION
if __name__ == "__main__":
    # datos de prueba (matriz)
    peliculas = [
        [1, "Spiderman Brand New Day", "Accion", 150],
        [2, "La Odisea", "Drama", 90],
        [3, "Supergirl", "Ciencia ficcion", 120],
        [4, "Mortal Kombat II", "Accion", 100],
        [5, "Maestros del Universo", "Aventura", 110]
    ]

    # Probando el encabezado
    imprimir_encabezado("El archivo de vista funciona")

    # Mensajes de colores
    imprimir_exito("Conexion establecida")
    imprimir_error("Archivo no encontrado")
    imprimir_advertencia("Quedan pocos intentos")

    # Impresion de la tabla
    print("\n--- MONSTRANDO CATALOGO DE PRUEBA ---")
    mostrar_catalogo(peliculas)
    