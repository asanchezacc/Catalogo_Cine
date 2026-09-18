import contextlib
import io

from src.datos import datos_iniciales
from src.modelos import usuarios, clientes
from src.funciones import peliculas, asientos, tickets, estadisticas, empleados
from src.validaciones import validar_contrasena
from src.vista import imprimir_encabezado, imprimir_exito, imprimir_error, mostrar_catalogo

PELICULAS = []
SALA = None

def inicializar():
    global SALA
    datos_iniciales.cargar_peliculas(PELICULAS)
    with contextlib.redirect_stdout(io.StringIO()):
        datos_iniciales.cargar_clientes()
    datos_iniciales.cargar_usuarios()
    SALA = asientos.crear_sala(datos_iniciales.SALA_FILAS, datos_iniciales.SALA_COLUMNAS)


def pedir_entero(mensaje):
    entrada = input(mensaje).strip()
    if not entrada.isdigit():
        return None
    return int(entrada)
def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def accion_ver_catalogo():
    mostrar_catalogo(empleados.ver_peliculas(PELICULAS))


def accion_ver_clientes():
    clientes_registrados = empleados.listar_clientes(mostrar_inactivos=False)
    if not clientes_registrados:
        print("No hay clientes para mostrar.")
        return
    for cliente in clientes_registrados:
        estado = "Activo" if cliente["estado"] else "Inactivo"
        print(
            f"ID {cliente['id']} - {cliente['nombre']} - "
            f"{cliente['email']} - {cliente['telefono']} - {estado}"
        )


def accion_dar_alta_cliente():
    nombre = input("Nombre del cliente: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()
    empleados.alta_cliente(nombre, email, telefono)


def accion_dar_baja_cliente():
    id_cliente = pedir_entero("ID del cliente a dar de baja: ")
    if id_cliente is None:
        imprimir_error("Ingresá un ID válido.")
        return
    empleados.baja_cliente(id_cliente)


def accion_ver_usuarios():
    for u in usuarios.usuarios:
        print(f"{u['usuario']} - {u['nombre']} - {u['rol']}")
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
def accion_ver_estadisticas():
    resumen = estadisticas.resumen_estadisticas(tickets.tickets_registrados)
    print(f"Precio promedio: ${resumen['promedio_precio']:.2f}")
    print(f"Tickets pendientes: {resumen['cantidad_pendientes']}")
    print(f"Tickets cobrados: {resumen['cantidad_cobrados']}")
    print(f"Tickets cancelados: {resumen['cantidad_cancelados']}")
    print(f"Porcentaje cobrados: {resumen['porcentaje_cobrados']:.1f}%")
    print(f"Total recaudado: ${resumen['total_recaudado']}")


def accion_ver_tickets():
    lista = empleados.ver_reservas()
    if not lista:
        print("No hay tickets para mostrar.")
        return
    lineas = map(
        lambda t: f"#{t['id']} - cliente {t['cliente_id']} - película {t['pelicula_id']} - asiento {t['asiento']} - ${t['precio']} - {t['estado']}",
        lista,
    )
    for linea in lineas:
        print(linea)


def accion_crear_ticket(usuario_actual):
    empleado = usuarios.buscar_usuario(usuario_actual)
    id_cliente = pedir_entero("ID del cliente: ")
    if id_cliente is None:
        imprimir_error("Ingresá un ID válido.")
        return
    if empleados.ver_cliente(id_cliente) is None:
        imprimir_error("No existe un cliente con ese ID.")
        return
    accion_ver_catalogo()
    id_pelicula = pedir_entero("ID de la película: ")
    if id_pelicula is None:
        imprimir_error("Ingresá un ID válido.")
        return
    pelicula = peliculas.obtener_pelicula(PELICULAS, id_pelicula)
    if pelicula is None:
        imprimir_error("Esa película no está en el catálogo.")
        return
    fila = pedir_entero(f"Fila del asiento (0 a {len(SALA)-1}): ")
    columna = pedir_entero(f"Columna del asiento (0 a {len(SALA[0])-1}): ")
    if fila is None or columna is None:
        imprimir_error("Ingresá números válidos para el asiento.")
        return

    exito, resultado = empleados.dar_reserva(
        SALA, id_cliente, id_pelicula, pelicula["precio"], fila, columna, empleado["id"]
    )
    if exito:
        imprimir_exito(f"Ticket #{resultado} creado.")
    else:
        imprimir_error(resultado)


def accion_cobrar_ticket():
    id_ticket = pedir_entero("Número de ticket a cobrar: ")
    if id_ticket is None:
        imprimir_error("Ingresá un número válido.")
        return
    exito, mensaje = empleados.cobrar_ticket(id_ticket)
    mostrar_resultado(exito, mensaje)


def accion_cancelar_ticket():
    id_ticket = pedir_entero("Número de ticket a cancelar: ")
    if id_ticket is None:
        imprimir_error("Ingresá un ID válido.")
        return
    exito, mensaje = empleados.cancelar_reserva(SALA, id_ticket)
    mostrar_resultado(exito, mensaje)


def accion_imprimir_ticket():
    id_ticket = pedir_entero("Número de ticket: ")
    if id_ticket is None:
        imprimir_error("Ingresá un número válido.")
        return
    datos = empleados.obtener_datos_ticket(id_ticket, PELICULAS)
    if datos is None:
        imprimir_error("Ese ticket no existe.")
        return
    print(f"--- Ticket #{datos['id']} ---")
    print(f"Cliente: {datos['cliente']}")
    print(f"Película: {datos['pelicula']}")
    print(f"Asiento: {datos['asiento']}")
    print(f"Precio: ${datos['precio']}")
    print(f"Estado: {datos['estado']}")


def accion_ver_asientos_ocupados():
    ocupados = empleados.asientos_ocupados(SALA)
    if not ocupados:
        print("No hay asientos ocupados.")
        return
    print("Asientos ocupados:")
    for fila, columna in sorted(ocupados):
        print(f"Fila {fila}, columna {columna}")


def accion_buscar_pelicula():
    texto = input("Texto del título a buscar: ").strip()
    resultados = empleados.buscar_pelicula(PELICULAS, texto)
    if not resultados:
        print("No se encontraron películas.")
        return
    for pelicula in resultados:
        print(f"ID {pelicula['id']} - {pelicula['titulo']}")


def accion_actualizar_cliente():
    id_cliente = pedir_entero("ID del cliente: ")
    if id_cliente is None:
        imprimir_error("Ingresá un ID válido.")
        return
    nombre = input("Nuevo nombre (Enter para conservarlo): ").strip() or None
    email = input("Nuevo email (Enter para conservarlo): ").strip() or None
    telefono = input("Nuevo teléfono (Enter para conservarlo): ").strip() or None
    empleados.actualizar_cliente(id_cliente, nombre, email, telefono)


def accion_listar_clientes():
    clientes_registrados = empleados.listar_clientes(mostrar_inactivos=False)
    if not clientes_registrados:
        print("No hay clientes registrados.")
        return
    for cliente in clientes_registrados:
        print(f"ID {cliente['id']} - {cliente['nombre']} - {cliente['email']}")


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
        print("12. Salir")
        opcion = input("Elegí una opción: ").strip()
        if opcion == "1": accion_ver_catalogo()
        elif opcion == "2": accion_ver_clientes()
        elif opcion == "3": accion_dar_alta_cliente()
        elif opcion == "4": accion_dar_baja_cliente()
        elif opcion == "5": accion_ver_usuarios()
        elif opcion == "6": accion_agregar_empleado()
        elif opcion == "7": accion_eliminar_empleado(usuario_actual, "administrador")
        elif opcion == "8": accion_ver_tickets()
        elif opcion == "9": accion_ver_historial()
        elif opcion == "10": accion_ver_estadisticas()
        elif opcion == "11": accion_cambiar_contrasena(usuario_actual)
        elif opcion == "12":
            print("Cerrando sesión.")
            continuar = False
        else:
            imprimir_error("Opción inválida.")

def menu_empleado(usuario_actual):
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
        print("10. Asientos ocupados")
        print("11. Buscar pelicula por titulo")
        print("12. Actualizar cliente")
        print("13. Ver clientes registrados")
        print("14. Salir")

        opcion = input("Elegí una opción: ").strip()
        if opcion == "1": accion_ver_catalogo()
        elif opcion == "2": accion_ver_clientes()
        elif opcion == "3": accion_dar_alta_cliente()
        elif opcion == "4": accion_dar_baja_cliente()
        elif opcion == "5": accion_crear_ticket(usuario_actual)
        elif opcion == "6": accion_cobrar_ticket()
        elif opcion == "7": accion_cancelar_ticket()
        elif opcion == "8": accion_imprimir_ticket()
        elif opcion == "9": accion_ver_tickets()
        elif opcion == "10": accion_ver_asientos_ocupados()
        elif opcion == "11": accion_buscar_pelicula()
        elif opcion == "12": accion_actualizar_cliente()
        elif opcion == "13": accion_listar_clientes()
        elif opcion == "14":
            print("Cerrando sesión.")
            continuar = False
        else:
            imprimir_error("Opción inválida.")
def main():
    imprimir_encabezado("Sistema de cine")
    inicializar()
    usuario, rol = usuarios.iniciar_sesion()
    if usuario is None:
        return
    if rol == "administrador":
        menu_administrador(usuario)
    elif rol == "empleado":
        menu_empleado(usuario)


if __name__ == "__main__":
    main()