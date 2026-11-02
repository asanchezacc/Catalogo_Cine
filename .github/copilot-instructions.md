# Instrucciones del proyecto Catalogo_Cine

Este proyecto debe desarrollarse respetando únicamente los contenidos de las
clases 1 a 13 de Programación I / Algoritmos y Estructuras de Datos I (UADE).
Todo se programa en Python 3.

## Contenidos permitidos

### Clases 1 a 6

- Listas, listas anidadas y matrices (listas de listas): creación estática,
  dinámica con `append()`, con `[0] * columnas` y por comprensión.
- Operaciones con matrices: suma, resta, multiplicación por escalar, totales por
  fila y columna, promedio y transpuesta.
- Índices (también negativos), recorridos con `for`, `while` y `for ... in`.
- Slicing `[inicio:fin:paso]`, rebanadas para reemplazar, eliminar e insertar,
  y copias de listas (`copy()`, `[:]`, `list()`).
- Listas por comprensión, con filtro `if` y con `if-else`.
- Métodos de listas: `append`, `extend`, `insert`, `remove`, `pop`, `clear`,
  `index`, `count`, `sort` (con `key` y `reverse`), `reverse`, `copy`.
- Funciones: `len`, `sum`, `min`, `max`, `list`, `range`, `abs`, `id`, `type`,
  `int`, `float`, `str`, `input`, `print` (con `end=`), `help`.
- Strings y sus métodos: `index`, `count`, `find`, `rfind`, `startswith`,
  `endswith`, `replace`, `strip`, `lstrip`, `rstrip`, `center`, `ljust`, `rjust`,
  `zfill`, `isalnum`, `isalpha`, `isnumeric`, `isdigit`, `isdecimal`, `isspace`,
  `islower`, `isupper`, `istitle`, `capitalize`, `title`, `lower`, `upper`,
  `swapcase`, `split`, `rsplit`, `splitlines`, `partition`, `rpartition`, `join`.
- Formato de cadenas: f-strings con ancho, alineación (`<`, `>`, `^`), relleno
  y decimales (`{x:.2f}`); también `%` y `.format()`. Secuencias de escape.
- Funciones con parámetros por omisión y argumentos pasados por nombre.
- Parámetros mutables e inmutables.
- Retornos múltiples y desempaquetado.
- Funciones lambda, invocación inmediata, `sort(key=...)` y `sorted(key=...)`.
- `map`, `filter` y `reduce` (`from functools import reduce`).
- Módulos y paquetes (`import`, `from ... import`, `__init__.py`).
- `if __name__ == "__main__":` con una función `main()`.
- Expresiones regulares con la biblioteca nativa `re`: `search`, `match`,
  `findall`, `sub`, `split`, `compile`, objeto `Match`, metacaracteres, grupos,
  rangos, clases predefinidas, cuantificadores y `re.IGNORECASE`.
- Diccionarios y listas de diccionarios: `keys`, `values`, `items`, `get`, `pop`,
  `setdefault`, `update`, `clear`, `copy`, `fromkeys`, `dict`, `zip`, `del`, `in`.
- Conversión de matriz a lista de diccionarios con `dict(zip(encabezados, fila))`.
- Tuplas: creación, operadores, tuplas de tuplas, slicing, `index` y `count`.
- Conjuntos (`set`): `add`, `remove`, `discard`, `clear`, `issubset` y
  operaciones `&`, `|`, `-`, `^`.
- Conversión entre tipos con `set()`, `list()` y `tuple()`.
- `random` (por ejemplo `random.randint`) cuando sea necesario cargar datos aleatorios.
- `math` (por ejemplo `math.pi`) si hace falta.
- Git y GitHub.

### Clases 8 y 9: estructura iterativa y excepciones

- `break` y `continue` (sin abusar), cláusula `else` del `while` y `while True`
  con `break` para repetir hasta un dato válido o un centinela.
- Tipos de error: sintaxis, tiempo de ejecución y semánticos.
- `try` / `except` / `else` / `finally`, varios `except` por tipo y `as` para
  nombrar la excepción.
- `raise` con mensaje (`ValueError`, `TypeError`, `Exception`) y `raise` solo
  para relanzar.
- `assert condicion, "mensaje"` y `AssertionError`.
- Validación de precondiciones y de la entrada del usuario.
- Excepciones usadas: `ValueError`, `TypeError`, `ZeroDivisionError`,
  `IndexError`, `KeyError`, `NameError`, `AssertionError`, `Exception`.

### Clase 10: pruebas unitarias

- Entornos: Desarrollo, Pruebas, Pre-Producción y Producción.
- Tipos de prueba: unitarias, de integración, de sistemas y de aceptación.
- pytest: archivos `test_*.py`, funciones `test_*` que solo usan `assert`,
  importando las funciones a probar (`from modulo import funcion`).
- Ejecución con `pytest`, `pytest -v` o `python -m pytest`.

### Clase 11: archivos de texto

- `open(nombre, modo, encoding="UTF-8")` con modos `r`, `w`, `a` (y `t`/`b`).
- Rutas con `\\`, `/` o cadena cruda `r"..."`.
- Apertura siempre dentro de `try`; cierre con `close()` en `finally` o con `with`.
- Escritura con `write()` y `writelines()` agregando `\n` a mano.
- Lectura solo con `readline()` (`while linea:`) o con `for linea in archivo:`.
- Procesar líneas con `strip()`, `rstrip()` y `split(";")`.
- Formatos: un campo por línea, separador `;`, columnas de ancho fijo.
- Excepciones: `FileNotFoundError` antes que `OSError`; también
  `PermissionError`, `IsADirectoryError`, `UnsupportedOperation`.
- CRUD sobre archivos: alta en modo `a`, baja y modificación con un archivo
  auxiliar temporal, y listado.

### Clase 12: archivos JSON

- `import json`: `dumps`, `loads`, `dump` (con `ensure_ascii=False, indent=4`) y `load`.
- CRUD con JSON: leer a memoria, modificar y sobrescribir el archivo en modo `w`.
- Excepciones: `except (FileNotFoundError, OSError, json.JSONDecodeError) as error:`.

### Clase 13: recursividad

- Caso base, caso recursivo y reducción del dominio.
- Pila de llamadas y `RecursionError`.
- Recursividad con números, listas (con rebanadas o con índice `i=0`),
  cadenas y matrices.
- Funciones recursivas que retornan valor y que no retornan valor.

## Requisitos del proyecto

- El código debe estar modularizado en archivos y paquetes reutilizables.
- Debe existir al menos un CRUD utilizando diccionarios o listas de diccionarios.
- Debe mantenerse al menos una entidad representada mediante matrices o listas
  de listas para comparar ambos enfoques.
- Deben utilizarse listas, diccionarios, tuplas y conjuntos de manera justificada.
- Las funciones lambda deben utilizarse para ordenar, filtrar o modificar datos.
- Deben utilizarse `map`, `filter` y `reduce` cuando corresponda.
- Las expresiones regulares deben utilizarse para validar datos como emails,
  fechas o códigos.
- Las salidas deben usar strings, f-strings y alineación cuando corresponda.
- El programa debe incluir los requisitos de matrices, como ordenar filas según
  una columna elegida por el usuario.
- Usar excepciones para prever datos erróneos del usuario, divisiones por cero
  y errores con archivos. El programa no debe romperse si el usuario ingresa
  una letra donde se espera un número: debe avisar y volver a pedir.
- Incluir pruebas unitarias con pytest en archivos `test_*.py`.
- Reemplazar los datos hardcodeados por archivos de texto (`.txt` con `;`) o
  JSON, manejando archivo inexistente, ruta inválida, permisos y datos mal
  formateados.
- Reemplazar funciones iterativas sobre listas o cadenas por versiones
  recursivas sin `for` ni `while`, indicando caso base, caso recursivo y
  reducción del dominio.
- El proyecto debe gestionarse con Git y GitHub mediante commits claros y ramas.

## Restricciones

- No usar clases, decoradores, generadores (`yield`), frameworks, bases de
  datos ni librerías externas que no aparezcan en las clases (pytest sí).
- No usar los módulos `csv`, `pathlib`, `os` ni `shutil`.
- No usar comprensión de diccionarios ni de conjuntos (solo de listas).
- No definir excepciones propias con `class`.
- En pytest no usar `pytest.raises`, *fixtures* ni `parametrize`: solo `assert`.
- No leer archivos de texto con `read()`, `read(n)` ni `readlines()`.
- No cargar todo un archivo de texto en memoria, no abrirlo y cerrarlo por cada
  registro y no recorrerlo más veces de las necesarias.
- No pedirle al usuario el nombre de un archivo.
- No usar `while True` para imitar un `for`.
- Evitar el `except:` sin tipo; si se usa, va último.
- No usar `assert` para manejar errores del usuario (es para depurar y probar).
- No usar `for` ni `while` dentro de las funciones recursivas pedidas.
- No incorporar conceptos avanzados que no estén incluidos en las clases sin
  avisar antes.
- No inventar funcionalidades que no sean necesarias para la consigna.
- Preferir soluciones simples, explicables y acordes al nivel de la materia.
- Mantener los nombres, estructuras y formatos ya utilizados por el proyecto.
- No modificar archivos de otros módulos sin necesidad.
- Antes de implementar una solución dudosa, explicar qué concepto utiliza y
  consultar si está permitido.

## Forma de trabajo

Antes de modificar código:

1. Revisar estas instrucciones.
2. Identificar qué requisito de las clases se está implementando.
3. Usar la solución más simple posible.
4. Explicar si se introduce una estructura o función nueva.

Al terminar un cambio, indicar qué archivos se modificaron y cómo probarlo.
