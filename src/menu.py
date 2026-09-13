from src.modelos.usuarios import buscar_usuario, agregar_usuario, eliminar_usuario, actualizar_usuario, iniciar_sesion, ver_historial
from src.validaciones import validar_contrasena
from src.funciones.peliculas import listar_peliculas, obtener_pelicula
from src.funciones.estadisticas import resumen_estadisticas
from src.datos.datos_iniciales import peliculas_iniciales, usuarios_iniciales
from src.modelos.clientes import alta_cliente, baja_cliente, buscar_cliente, mostrar_clientes
from src.funciones.tickets import crear_ticket, cobrar, cancelar_ticket, obtener_ticket, tickets_registrados
from src.vista import imprimir_encabezado, imprimir_exito, imprimir_error, mostrar_catalogo

PELICULAS = [p.copy() for p in peliculas_iniciales]
USUARIOS = [u.copy() for u in usuarios_iniciales]


def pedir_entero(mensaje):
    entrada = input(mensaje).strip()
    if not entrada.isdigit():
        return None
    return int(entrada)


def obtener_id_empleado(usuario_actual):
    # PROVISORIO: uso la posición en la lista como ID numérico, porque
    # usuarios.py identifica empleados por nombre de usuario, no por ID,
    # y tickets.py pide un empleado_id numérico. Avisarle al grupo.
    for i, u in enumerate(USUARIOS):
        if u["usuario"] == usuario_actual:
            return i + 1
    return None


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def accion_ver_catalogo():
    mostrar_catalogo(PELICULAS)


def accion_ver_clientes():
    mostrar_clientes()


def accion_dar_alta_cliente():
    nombre = input("Nombre del cliente: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()
    alta_cliente(nombre, email, telefono)


def accion_dar_baja_cliente():
    id_cliente = pedir_entero("ID del cliente a dar de baja: ")
    if id_cliente is None:
        imprimir_error("Ingresá un ID válido.")
        return
    baja_cliente(id_cliente)


def accion_ver_usuarios():
    for u in USUARIOS:
        print(f"{u['usuario']} - {u['rol']}")


def accion_agregar_usuario(usuario_actual):
    nuevo_usuario = input("Nombre de usuario nuevo: ").strip()
    if not nuevo_usuario:
        imprimir_error("El nombre de usuario no puede estar vacío.")
        return
    contrasena = input("Contraseña: ")
    es_valida, mensaje = validar_contrasena(contrasena)
    if not es_valida:
        imprimir_error(mensaje)
        return
    exito, mensaje = agregar_usuario(usuario_actual, nuevo_usuario, contrasena, "empleado", USUARIOS)
    mostrar_resultado(exito, mensaje)


def accion_eliminar_usuario(usuario_actual):
    usuario_a_borrar = input("Usuario a borrar: ").strip()
    exito, mensaje = eliminar_usuario(usuario_actual, usuario_a_borrar, USUARIOS)
    mostrar_resultado(exito, mensaje)


def accion_cambiar_contrasena(usuario_actual):
    nueva_contrasena = input("Nueva contraseña: ")
    es_valida, mensaje = validar_contrasena(nueva_contrasena)
    if not es_valida:
        imprimir_error(mensaje)
        return
    exito, mensaje = actualizar_usuario(usuario_actual, usuario_actual, nueva_contrasena, USUARIOS)
    mostrar_resultado(exito, mensaje)


def accion_ver_historial():
    entradas = ver_historial()
    if not entradas:
        print("No hay historial todavía.")
        return
    for accion, usuario, rol in entradas:
        print(f"{accion} - {usuario} ({rol})")


def accion_ver_estadisticas():
    resumen = resumen_estadisticas(tickets_registrados)
    print(f"Precio promedio: ${resumen['promedio_precio']:.2f}")
    print(f"Tickets pendientes: {resumen['cantidad_pendientes']}")
    print(f"Tickets cobrados: {resumen['cantidad_cobrados']}")
    print(f"Tickets cancelados: {resumen['cantidad_cancelados']}")
    print(f"Porcentaje cobrados: {resumen['porcentaje_cobrados']:.1f}%")
    print(f"Total recaudado: ${resumen['total_recaudado']}")


def accion_ver_tickets(id_empleado=None):
    tickets = tickets_registrados
    if id_empleado is not None:
        tickets = list(filter(lambda t: t["empleado_id"] == id_empleado, tickets))
    if not tickets:
        print("No hay tickets para mostrar.")
        return
    lineas = map(
        lambda t: f"#{t['id']} - cliente {t['cliente_id']} - película {t['pelicula_id']} - asiento {t['asiento']} - ${t['precio']} - {t['estado']}",
        tickets,
    )
    for linea in lineas:
        print(linea)


def accion_crear_ticket(usuario_actual):
    id_empleado = obtener_id_empleado(usuario_actual)

    id_cliente = pedir_entero("ID del cliente: ")
    if id_cliente is None:
        imprimir_error("Ingresá un ID válido.")
        return
    if buscar_cliente(id_cliente) is None:
        imprimir_error("No existe un cliente con ese ID.")
        return

    accion_ver_catalogo()
    id_pelicula = pedir_entero("ID de la película: ")
    if id_pelicula is None:
        imprimir_error("Ingresá un ID válido.")
        return
    pelicula = obtener_pelicula(PELICULAS, id_pelicula)
    if pelicula is None:
        imprimir_error("Esa película no está en el catálogo.")
        return

    fila = pedir_entero("Fila del asiento: ")
    columna = pedir_entero("Columna del asiento: ")
    if fila is None or columna is None:
        imprimir_error("Ingresá números válidos para el asiento.")
        return

    exito, resultado = crear_ticket(id_cliente, id_pelicula, (fila, columna), pelicula["precio"], id_empleado)
    if exito:
        imprimir_exito(f"Ticket #{resultado} creado.")
    else:
        imprimir_error(resultado)


def accion_cobrar_ticket():
    id_ticket = pedir_entero("Número de ticket a cobrar: ")
    if id_ticket is None:
        imprimir_error("Ingresá un número válido.")
        return
    exito, mensaje = cobrar(id_ticket)
    mostrar_resultado(exito, mensaje)


def accion_cancelar_ticket():
    id_ticket = pedir_entero("Número de ticket a cancelar: ")
    if id_ticket is None:
        imprimir_error("Ingresá un número válido.")
        return
    exito, mensaje = cancelar_ticket(id_ticket)
    mostrar_resultado(exito, mensaje)


def accion_imprimir_ticket():
    id_ticket = pedir_entero("Número de ticket: ")
    if id_ticket is None:
        imprimir_error("Ingresá un número válido.")
        return
    ticket = obtener_ticket(id_ticket)
    if ticket is None:
        imprimir_error("Ese ticket no existe.")
        return
    pelicula = obtener_pelicula(PELICULAS, ticket["pelicula_id"])
    cliente = buscar_cliente(ticket["cliente_id"])
    titulo = pelicula["titulo"] if pelicula else "?"
    nombre_cliente = cliente["nombre"] if cliente else "?"
    print(f"--- Ticket #{ticket['id']} ---")
    print(f"Cliente: {nombre_cliente}")
    print(f"Película: {titulo}")
    print(f"Asiento: {ticket['asiento']}")
    print(f"Precio: ${ticket['precio']}")
    print(f"Estado: {ticket['estado']}")


def menu_administrador(usuario_actual):
    while True:
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
        print("12. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            accion_ver_catalogo()
        elif opcion == "2":
            accion_ver_clientes()
        elif opcion == "3":
            accion_dar_alta_cliente()
        elif opcion == "4":
            accion_dar_baja_cliente()
        elif opcion == "5":
            accion_ver_usuarios()
        elif opcion == "6":
            accion_agregar_usuario(usuario_actual)
        elif opcion == "7":
            accion_eliminar_usuario(usuario_actual)
        elif opcion == "8":
            accion_ver_tickets()
        elif opcion == "9":
            accion_ver_historial()
        elif opcion == "10":
            accion_ver_estadisticas()
        elif opcion == "11":
            accion_cambiar_contrasena(usuario_actual)
        elif opcion == "12":
            print("Cerrando sesión.")
            break
        else:
            imprimir_error("Opción inválida.")


def menu_empleado(usuario_actual):
    while True:
        imprimir_encabezado("Menú empleado")
        print("1. Ver catálogo de películas")
        print("2. Ver clientes")
        print("3. Dar de alta un cliente")
        print("4. Dar de baja un cliente")
        print("5. Dar una reserva")
        print("6. Cobrar un ticket")
        print("7. Cancelar un ticket")
        print("8. Imprimir ticket")
        print("9. Ver todos los tickets")
        print("10. Darme de baja")
        print("11. Cambiar mi contraseña")
        print("12. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            accion_ver_catalogo()
        elif opcion == "2":
            accion_ver_clientes()
        elif opcion == "3":
            accion_dar_alta_cliente()
        elif opcion == "4":
            accion_dar_baja_cliente()
        elif opcion == "5":
            accion_crear_ticket(usuario_actual)
        elif opcion == "6":
            accion_cobrar_ticket()
        elif opcion == "7":
            accion_cancelar_ticket()
        elif opcion == "8":
            accion_imprimir_ticket()
        elif opcion == "9":
            accion_ver_tickets()
        elif opcion == "10":
            exito, mensaje = eliminar_usuario(usuario_actual, usuario_actual, USUARIOS)
            mostrar_resultado(exito, mensaje)
            if exito:
                break
        elif opcion == "11":
            accion_cambiar_contrasena(usuario_actual)
        elif opcion == "12":
            print("Cerrando sesión.")
            break
        else:
            imprimir_error("Opción inválida.")


def main():
    usuario, rol = iniciar_sesion(USUARIOS)

    if usuario is None:
        return

    if rol == "admin":
        menu_administrador(usuario)
    elif rol == "empleado":
        menu_empleado(usuario)


if __name__ == "__main__":
    main()
