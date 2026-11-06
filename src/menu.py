

from src.datos import datos_iniciales
from src.modelos import usuarios, clientes
from src.funciones import peliculas, asientos, tickets, estadisticas, empleados
from src.validaciones import validar_contrasena
from src.vista import imprimir_encabezado, imprimir_exito, imprimir_error, mostrar_catalogo, mostrar_tabla

PELICULAS = []


def inicializar():
    if datos_iniciales.cargar_peliculas(PELICULAS) is None:
        imprimir_error("No se pudieron cargar las películas. Revisá peliculas.json.")
        return None
    # Si el JSON está dañado, no se reemplaza con clientes de prueba.
    estado_clientes = clientes.cargar_clientes_desde_json()
    if estado_clientes is False:
        return None
    if estado_clientes is None:
        cantidad = datos_iniciales.cargar_clientes()
        if cantidad != len(datos_iniciales.CLIENTES_INICIALES):
            imprimir_error("No se pudieron crear los clientes iniciales.")
            return None
    exito, mensaje = datos_iniciales.inicializar_usuarios()
    if not exito:
        imprimir_error(mensaje)
        return None

    sala = asientos.crear_sala(
        datos_iniciales.SALA_FILAS,
        datos_iniciales.SALA_COLUMNAS
    )

    # Se recuperan los tickets del archivo y se vuelven a ocupar sus asientos
    exito, mensaje = tickets.cargar_tickets()
    if not exito:
        imprimir_error(mensaje)
        return None
    exito, mensaje = asientos.reconstruir_ocupacion(sala, tickets.tickets_registrados)
    if not exito:
        imprimir_error(mensaje)
        return None

    return sala


def pedir_entero(mensaje):
    """
    pre: recibe el mensaje a mostrar.
    pos: devuelve un número entero. Si el usuario ingresa algo que no es
    un número (por ejemplo una letra), avisa y lo vuelve a pedir.
    """
    while True:
        try:
            numero = int(input(mensaje).strip())
            break
        except ValueError:
            imprimir_error("Error: se esperaba un número entero. Volvé a intentarlo.")
    return numero


def pedir_entero_opcional(mensaje):
    """
    pre: recibe el mensaje a mostrar.
    pos: devuelve None si el usuario aprieta Enter sin escribir nada,
    o un número entero. Si ingresa algo que no es un número, lo vuelve a pedir.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            numero = None
            break
        try:
            numero = int(entrada)
            break
        except ValueError:
            imprimir_error("Error: se esperaba un número entero. Volvé a intentarlo.")
    return numero


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def accion_ver_catalogo():
    mostrar_catalogo(empleados.ver_peliculas(PELICULAS))


def accion_ver_clientes():
    # La tabla y el conteo muestran únicamente los clientes activos.
    clientes.mostrar_clientes()
    activos = empleados.listar_clientes()
    cantidad = clientes.contar_clientes_recursivo(activos)
    print(f"Clientes activos: {cantidad}")


def accion_dar_alta_cliente():
    nombre = input("Nombre del cliente: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()
    empleados.alta_cliente(nombre, email, telefono)


def accion_dar_baja_cliente():
    id_cliente = pedir_entero("ID del cliente a dar de baja: ")
    empleados.baja_cliente(id_cliente)


def accion_ver_usuarios():
    columnas = [
        ("Usuario", "usuario", 15),
        ("Nombre", "nombre", 25),
        ("Rol", "rol", 15),
    ]
    mostrar_tabla(usuarios.usuarios, columnas)


def accion_agregar_empleado():
    nombre = input("Nombre completo: ").strip()
    nuevo_usuario = input("Nombre de usuario: ").strip()
    if not nuevo_usuario:
        imprimir_error("El nombre de usuario no puede estar vacío.")
        return
    contrasena = input("Contraseña: ")
    es_valida, mensaje = validar_contrasena(contrasena)
    if not es_valida:
        imprimir_error(mensaje)
        return
    exito, resultado = usuarios.alta_usuario(nombre, nuevo_usuario, contrasena, "empleado")
    if exito:
        imprimir_exito(f"Empleado '{nuevo_usuario}' agregado.")
    else:
        imprimir_error(resultado)


def accion_eliminar_empleado(usuario_actual, rol_actual):
    usuario_a_borrar = input("Usuario a borrar: ").strip()
    objetivo = usuarios.buscar_usuario(usuario_a_borrar)
    if objetivo is None:
        imprimir_error("Ese usuario no existe.")
        return
    if objetivo["rol"] == "administrador":
        imprimir_error("No se puede borrar a un administrador.")
        return
    if rol_actual == "empleado" and usuario_a_borrar != usuario_actual:
        imprimir_error("Como empleado, solo podés darte de baja a vos mismo.")
        return
    exito, mensaje = usuarios.baja_usuario(usuario_a_borrar)
    mostrar_resultado(exito, mensaje)

def accion_cambiar_contrasena(usuario_actual):
    nueva_contrasena = input("Nueva contraseña: ")
    es_valida, mensaje = validar_contrasena(nueva_contrasena)
    if not es_valida:
        imprimir_error(mensaje)
        return
    exito, mensaje = usuarios.actualizar_contrasena(usuario_actual, nueva_contrasena)
    mostrar_resultado(exito, mensaje)


def accion_ver_historial():
    entradas = usuarios.ver_historial()
    if not entradas:
        print("No hay historial todavía.")
        return
    for accion, usuario, rol in entradas:
        print(f"{accion} - {usuario} ({rol})")


def titulos_de_ids(ids, lista_peliculas):
    """Devuelve los títulos de las películas cuyos IDs están en el conjunto recibido."""
    return [pelicula["titulo"] for pelicula in lista_peliculas if pelicula["id"] in ids]


def accion_ver_estadisticas():
    lista_tickets = tickets.tickets_registrados

    imprimir_encabezado("Resumen de tickets")
    resumen = estadisticas.resumen_estadisticas(lista_tickets)
    print(f"Precio promedio: ${resumen['promedio_precio']:.2f}")
    print(f"Tickets pendientes: {resumen['cantidad_pendientes']}")
    print(f"Tickets cobrados: {resumen['cantidad_cobrados']}")
    print(f"Tickets cancelados: {resumen['cantidad_cancelados']}")
    print(f"Porcentaje cobrados: {resumen['porcentaje_cobrados']:.1f}%")
    # El total visible se calcula recursivamente con los tickets cobrados.
    total_recursivo = tickets.sumar_recaudacion_recursiva(lista_tickets)
    print(f"Total recaudado: ${total_recursivo:.2f}")

    imprimir_encabezado("Ventas por película")
    if resumen["cantidad_cobrados"] == 0:
        print("Todavía no hay tickets cobrados.")
    else:
        mas_vendida, menos_vendida = estadisticas.peliculas_mas_y_menos_vendidas(PELICULAS, lista_tickets)
        if mas_vendida is not None:
            print(f"Más vendida: {mas_vendida[0]} ({mas_vendida[1]} tickets cobrados)")
            print(f"Menos vendida: {menos_vendida[0]} ({menos_vendida[1]} tickets cobrados)")

        print("Ranking de las 3 más vendidas:")
        posicion = 1
        for titulo, cantidad in estadisticas.ranking_peliculas_mas_vendidas(PELICULAS, lista_tickets):
            print(f"  {posicion}. {titulo:<25} {cantidad:>3} tickets")
            posicion += 1

        # Conjuntos: interseccion y diferencia hechas en estadisticas.py
        con_ventas, sin_ventas = estadisticas.clasificar_peliculas_por_ventas(PELICULAS, lista_tickets)
        print(f"Con ventas: {', '.join(titulos_de_ids(con_ventas, PELICULAS))}")
        if len(sin_ventas) == 0:
            print("Sin ventas: ninguna")
        else:
            print(f"Sin ventas: {', '.join(titulos_de_ids(sin_ventas, PELICULAS))}")

    imprimir_encabezado("Datos del catálogo")
    print(f"Películas en cartelera: {peliculas.contar_peliculas(PELICULAS)}")
    print(f"Duración promedio: {peliculas.promedio_duracion(PELICULAS):.1f} minutos")

    imprimir_encabezado("Precio promedio por género")
    promedios = estadisticas.promedio_precio_por_genero(PELICULAS)
    for genero, promedio in promedios.items():
        print(f"{genero:<20} ${promedio:>9.2f}")


def linea_ticket(ticket):
    """Arma la línea de un ticket con el nombre del cliente y el título de la película."""
    cliente = empleados.ver_cliente(ticket["cliente_id"])
    pelicula = peliculas.obtener_pelicula(PELICULAS, ticket["pelicula_id"])
    nombre = "?"
    if cliente is not None:
        # Slicing para que el nombre y el título no se pasen de su columna
        nombre = cliente["nombre"][:19]
    titulo = "?"
    if pelicula is not None:
        titulo = pelicula["titulo"][:24]
    fila, columna = ticket["asiento"]
    linea = f"#{ticket['id']:<4}{nombre:<20}{titulo:<25}"
    linea = linea + f"fila {fila} col {columna}  ${ticket['precio']:>9.2f}  {ticket['estado']}"
    return linea


def mostrar_lista_tickets(lista):
    """Muestra una lista de tickets, uno por línea."""
    if len(lista) == 0:
        print("No hay tickets para mostrar.")
        return
    lineas = list(map(linea_ticket, lista))
    for linea in lineas:
        print(linea)


def accion_ver_tickets():
    mostrar_lista_tickets(empleados.ver_reservas())


def tickets_de_pelicula(id_pelicula, lista_tickets):
    """Devuelve los tickets que corresponden a una película."""
    return list(filter(lambda t: t["pelicula_id"] == id_pelicula, lista_tickets))


def tickets_activos_de_pelicula(id_pelicula, lista_tickets):
    """Devuelve los tickets pendientes o cobrados de una película (no los cancelados)."""
    return list(filter(lambda t: t["estado"] != "cancelado", tickets_de_pelicula(id_pelicula, lista_tickets)))


def accion_ver_tickets_de_cliente():
    id_cliente = pedir_entero("ID del cliente: ")
    cliente = empleados.ver_cliente(id_cliente)
    if cliente is None:
        imprimir_error("No existe un cliente con ese ID.")
        return
    imprimir_encabezado(f"Tickets de {cliente['nombre']}")
    mostrar_lista_tickets(clientes.obtener_tickets_de_cliente(id_cliente, tickets.tickets_registrados))


def accion_ver_tickets_de_pelicula():
    accion_ver_catalogo()
    id_pelicula = pedir_entero("ID de la película: ")
    pelicula = peliculas.obtener_pelicula(PELICULAS, id_pelicula)
    if pelicula is None:
        imprimir_error("Esa película no está en el catálogo.")
        return
    imprimir_encabezado(f"Tickets de {pelicula['titulo']}")
    mostrar_lista_tickets(tickets_de_pelicula(id_pelicula, tickets.tickets_registrados))


def proximo_id_pelicula(lista_peliculas):
    """Devuelve el ID que le corresponde a una película nueva."""
    if len(lista_peliculas) == 0:
        return 1
    ids = [pelicula["id"] for pelicula in lista_peliculas]
    return max(ids) + 1


def recortar_titulo(titulo):
    """
    Recorta el título igual que peliculas.py al guardarlo:
    si tiene más de 50 caracteres, deja los primeros 47 y agrega "...".
    """
    if len(titulo) > 50:
        return titulo[:47] + "..."
    return titulo


def titulo_repetido(titulo, lista_peliculas, id_excluido=None):
    """
    pre: recibe un título, la lista de películas y opcionalmente el ID de una
    película que no se tiene en cuenta (la que se está modificando).
    pos: devuelve True si otra película ya tiene ese título (sin importar mayúsculas).
    Compara el título ya recortado, porque así queda guardado.
    """
    titulo = recortar_titulo(titulo)
    for pelicula in lista_peliculas:
        if pelicula["id"] != id_excluido and pelicula["titulo"].lower() == titulo.lower():
            return True
    return False


def accion_alta_pelicula():
    titulo = input("Título: ").strip()
    if titulo == "":
        imprimir_error("El título no puede estar vacío.")
        return
    if titulo_repetido(titulo, PELICULAS):
        imprimir_error("Ya existe una película con ese título.")
        return
    genero = input("Género: ").strip()
    if genero == "":
        imprimir_error("El género no puede estar vacío.")
        return
    duracion = pedir_entero("Duración (en minutos): ")
    precio = pedir_entero("Precio: ")
    if duracion <= 0 or precio <= 0:
        imprimir_error("La duración y el precio deben ser mayores que cero.")
        return
    id_pelicula = proximo_id_pelicula(PELICULAS)
    if peliculas.agregar_pelicula(PELICULAS, id_pelicula, titulo, genero, duracion, precio):
        imprimir_exito(f"Película '{recortar_titulo(titulo)}' agregada con ID {id_pelicula}.")
    else:
        # El ID siempre es nuevo, así que si falla es porque no se pudo guardar el JSON
        imprimir_error("No se pudo guardar la película en el archivo.")


def accion_modificar_pelicula():
    accion_ver_catalogo()
    id_pelicula = pedir_entero("ID de la película a modificar: ")
    if peliculas.obtener_pelicula(PELICULAS, id_pelicula) is None:
        imprimir_error("Esa película no está en el catálogo.")
        return
    # Si el usuario aprieta Enter se usa None, y actualizar_pelicula conserva ese dato
    titulo = input("Nuevo título (Enter para conservarlo): ").strip()
    if titulo == "":
        titulo = None
    elif titulo_repetido(titulo, PELICULAS, id_pelicula):
        imprimir_error("Ya existe otra película con ese título.")
        return
    genero = input("Nuevo género (Enter para conservarlo): ").strip()
    if genero == "":
        genero = None
    duracion = pedir_entero_opcional("Nueva duración (Enter para conservarla): ")
    if duracion != None and duracion <= 0:
        imprimir_error("La duración debe ser mayor que cero.")
        return
    precio = pedir_entero_opcional("Nuevo precio (Enter para conservarlo): ")
    if precio != None and precio <= 0:
        imprimir_error("El precio debe ser mayor que cero.")
        return
    if titulo == None and genero == None and duracion == None and precio == None:
        print("No se cambió ningún dato.")
        return
    if peliculas.actualizar_pelicula(PELICULAS, id_pelicula, titulo, genero, duracion, precio):
        imprimir_exito(f"Película ID {id_pelicula} modificada.")
    else:
        imprimir_error("No se pudo guardar el cambio en el archivo.")


def accion_baja_pelicula():
    accion_ver_catalogo()
    id_pelicula = pedir_entero("ID de la película a dar de baja: ")
    if peliculas.obtener_pelicula(PELICULAS, id_pelicula) is None:
        imprimir_error("Esa película no está en el catálogo.")
        return
    activos = tickets_activos_de_pelicula(id_pelicula, tickets.tickets_registrados)
    if len(activos) > 0:
        imprimir_error(f"No se puede dar de baja: tiene {len(activos)} ticket(s) pendientes o cobrados.")
        return
    if peliculas.eliminar_pelicula(PELICULAS, id_pelicula):
        imprimir_exito(f"Película ID {id_pelicula} eliminada del catálogo.")
    else:
        imprimir_error("No se pudo guardar el cambio en el archivo.")


def accion_crear_ticket(usuario_actual, sala):
    empleado = usuarios.buscar_usuario(usuario_actual)
    id_cliente = pedir_entero("ID del cliente: ")
    cliente = empleados.ver_cliente(id_cliente)
    if cliente is None:
        imprimir_error("No existe un cliente con ese ID.")
        return
    if cliente["estado"] == False:
        imprimir_error("Ese cliente está dado de baja. No se le pueden hacer reservas.")
        return
    accion_ver_catalogo()
    id_pelicula = pedir_entero("ID de la película: ")
    pelicula = peliculas.obtener_pelicula(PELICULAS, id_pelicula)
    if pelicula is None:
        imprimir_error("Esa película no está en el catálogo.")
        return
    mostrar_grilla_sala(sala)
    fila = pedir_entero(f"Fila del asiento (0 a {len(sala)-1}): ")
    columna = pedir_entero(f"Columna del asiento (0 a {len(sala[0])-1}): ")

    exito, resultado = empleados.dar_reserva(sala, id_cliente, id_pelicula, pelicula["precio"], fila, columna, empleado["id"])
    if exito:
        imprimir_exito(f"Ticket #{resultado} creado.")
    else:
        imprimir_error(resultado)


def accion_cobrar_ticket():
    id_ticket = pedir_entero("Número de ticket a cobrar: ")
    exito, mensaje = empleados.cobrar_ticket(id_ticket)
    mostrar_resultado(exito, mensaje)


def accion_cancelar_ticket(sala):
    id_ticket = pedir_entero("Número de ticket a cancelar: ")
    exito, mensaje = empleados.cancelar_reserva(sala, id_ticket)
    mostrar_resultado(exito, mensaje)


def accion_imprimir_ticket():
    id_ticket = pedir_entero("Número de ticket: ")
    datos = empleados.obtener_datos_ticket(id_ticket, PELICULAS)
    if datos is None:
        imprimir_error("Ese ticket no existe.")
        return
    print(f"--- Ticket #{datos['id']} ---")
    print(f"Cliente: {datos['cliente']}")
    print(f"Película: {datos['pelicula']}")
    print(f"Asiento: {datos['asiento']}")
    print(f"Precio: ${datos['precio']:.2f}")
    print(f"Estado: {datos['estado']}")


def armar_grilla_sala(mapa, filas, columnas):
    """
    pre: recibe el diccionario de mapa_ocupacion ({(fila, columna): "Libre"/"Ocupado"})
    y la cantidad de filas y columnas de la sala.
    pos: devuelve una lista de cadenas, una por cada línea de la grilla.
    Usa los mismos números de fila y columna que se piden al reservar.
    """
    lineas = []
    encabezado = "      "
    for columna in range(columnas):
        encabezado += f"{columna:>3}"
    lineas.append(encabezado)

    for fila in range(filas):
        linea = f"Fila {fila}"
        for columna in range(columnas):
            if mapa[(fila, columna)] == "Ocupado":
                linea += "  X"
            else:
                linea += "  -"
        lineas.append(linea)
    return lineas


def mostrar_grilla_sala(sala):
    """Muestra la sala como una grilla usando mapa_ocupacion."""
    if len(sala) == 0:
        imprimir_error("La sala no tiene asientos.")
        return
    mapa = empleados.mapa_ocupacion(sala)
    filas = len(sala)
    columnas = len(sala[0])

    imprimir_encabezado("Sala")
    print("PANTALLA".center(6 + columnas * 3))
    for linea in armar_grilla_sala(mapa, filas, columnas):
        print(linea)
    print("  - Libre    X Ocupado")
    print(f"Asientos libres: {asientos.contar_asientos_libres(sala)}")


def accion_ver_asientos_ocupados(sala):
    mostrar_grilla_sala(sala)


def accion_buscar_pelicula():
    texto = input("Texto del título a buscar: ").strip()
    resultados = empleados.buscar_pelicula(PELICULAS, texto)
    if len(resultados) == 0:
        print("No se encontraron películas.")
        return
    mostrar_catalogo(resultados)


def accion_actualizar_cliente():
    id_cliente = pedir_entero("ID del cliente: ")
    nombre = input("Nuevo nombre (Enter para conservarlo): ").strip()
    if nombre == "":
        nombre = None
    email = input("Nuevo email (Enter para conservarlo): ").strip()
    if email == "":
        email = None
    telefono = input("Nuevo teléfono (Enter para conservarlo): ").strip()
    if telefono == "":
        telefono = None
    empleados.actualizar_cliente(id_cliente, nombre, email, telefono)


# Tupla: los campos por los que se puede ordenar no cambian
CAMPOS_ORDEN_CLIENTES = ("id", "nombre", "email", "estado")


def clientes_para_tabla(lista_clientes):
    """Devuelve copias de los clientes con el estado como texto (Activo/Inactivo)."""
    resultado = []
    for cliente in lista_clientes:
        copia = cliente.copy()
        if cliente["estado"]:
            copia["estado"] = "Activo"
        else:
            copia["estado"] = "Inactivo"
        resultado.append(copia)
    return resultado


def accion_ordenar_clientes():
    print("Ordenar por: 1. ID   2. Nombre   3. Email   4. Estado")
    opcion = pedir_entero("Elegí la columna: ")
    if opcion < 1 or opcion > len(CAMPOS_ORDEN_CLIENTES):
        imprimir_error("Opción inválida.")
        return
    campo = CAMPOS_ORDEN_CLIENTES[opcion - 1]
    respuesta = input("¿De mayor a menor? (s/n): ").strip().lower()
    ordenados = clientes.ordenar_clientes(campo, respuesta == "s")
    columnas = [
        ("ID", "id", 5),
        ("Nombre", "nombre", 25),
        ("Email", "email", 30),
        ("Telefono", "telefono", 15),
        ("Estado", "estado", 10),
    ]
    imprimir_encabezado(f"Clientes ordenados por {campo}")
    mostrar_tabla(clientes_para_tabla(ordenados), columnas)


def accion_listar_clientes():
    # La opción 2 muestra solo los activos; esta muestra también los dados de baja
    clientes.mostrar_clientes(mostrar_inactivos=True)


def menu_administrador(usuario_actual):
    continuar = True
    while continuar:
        imprimir_encabezado("Menú administrador")
        print("1. Ver catálogo de películas")
        print("2. Ver clientes")
        print("3. Dar de alta un cliente")
        print("4. Dar de baja un cliente")
        print("5. Ver usuarios")
        print("6. Dar de alta un empleado")
        print("7. Borrar un empleado")
        print("8. Ver todos los tickets")
        print("9. Ver historial de usuarios")
        print("10. Ver estadísticas")
        print("11. Cambiar mi contraseña")
        print("12. Alta de película")
        print("13. Modificar película")
        print("14. Baja de película")
        print("15. Ver tickets de un cliente")
        print("16. Ver tickets de una película")
        print("17. Ordenar clientes")
        print("18. Salir")
        opcion = pedir_entero("Elegí una opción: ")
        if opcion == 1: accion_ver_catalogo()
        elif opcion == 2: accion_ver_clientes()
        elif opcion == 3: accion_dar_alta_cliente()
        elif opcion == 4: accion_dar_baja_cliente()
        elif opcion == 5: accion_ver_usuarios()
        elif opcion == 6: accion_agregar_empleado()
        elif opcion == 7: accion_eliminar_empleado(usuario_actual, "administrador")
        elif opcion == 8: accion_ver_tickets()
        elif opcion == 9: accion_ver_historial()
        elif opcion == 10: accion_ver_estadisticas()
        elif opcion == 11: accion_cambiar_contrasena(usuario_actual)
        elif opcion == 12: accion_alta_pelicula()
        elif opcion == 13: accion_modificar_pelicula()
        elif opcion == 14: accion_baja_pelicula()
        elif opcion == 15: accion_ver_tickets_de_cliente()
        elif opcion == 16: accion_ver_tickets_de_pelicula()
        elif opcion == 17: accion_ordenar_clientes()
        elif opcion == 18:
            print("Cerrando sesión.")
            continuar = False
        else:
            imprimir_error("Opción inválida.")

def menu_empleado(usuario_actual, sala):
    continuar = True
    while continuar:
        imprimir_encabezado("Menú empleado")
        print("1. Ver catálogo de películas")
        print("2. Ver clientes")
        print("3. Dar de alta un cliente")
        print("4. Dar de baja un cliente")
        print("5. Dar una reserva")
        print("6. Cobrar un ticket")
        print("7. Cancelar reserva")
        print("8. Imprimir ticket")
        print("9. Ver todos los tickets")
        print("10. Ver sala (asientos ocupados)")
        print("11. Buscar pelicula por titulo")
        print("12. Actualizar cliente")
        print("13. Ver todos los clientes (incluye dados de baja)")
        print("14. Ver tickets de un cliente")
        print("15. Ver tickets de una película")
        print("16. Salir")

        opcion = pedir_entero("Elegí una opción: ")
        if opcion == 1: accion_ver_catalogo()
        elif opcion == 2: accion_ver_clientes()
        elif opcion == 3: accion_dar_alta_cliente()
        elif opcion == 4: accion_dar_baja_cliente()
        elif opcion == 5: accion_crear_ticket(usuario_actual, sala)
        elif opcion == 6: accion_cobrar_ticket()
        elif opcion == 7: accion_cancelar_ticket(sala)
        elif opcion == 8: accion_imprimir_ticket()
        elif opcion == 9: accion_ver_tickets()
        elif opcion == 10: accion_ver_asientos_ocupados(sala)
        elif opcion == 11: accion_buscar_pelicula()
        elif opcion == 12: accion_actualizar_cliente()
        elif opcion == 13: accion_listar_clientes()
        elif opcion == 14: accion_ver_tickets_de_cliente()
        elif opcion == 15: accion_ver_tickets_de_pelicula()
        elif opcion == 16:
            print("Cerrando sesión.")
            continuar = False
        else:
            imprimir_error("Opción inválida.")
def main():
    imprimir_encabezado("Sistema de cine")
    sala = inicializar()
    if sala is None:
        return
    usuario, rol = usuarios.iniciar_sesion()
    if usuario is None:
        return
    if rol == "administrador":
        menu_administrador(usuario)
    elif rol == "empleado":
        menu_empleado(usuario, sala)


if __name__ == "__main__":
    main()
