from tabulate import tabulate

ENCABEZADOS_REGISTROS = ["Departamento", "Municipio", "Cultivo", "Topografía"]
TEXTO_SIN_DATOS = "Sin datos"


def mostrar_titulo():
    print("=" * 60)
    print("  CONSULTA DE VARIABLES EDÁFICAS - SUELOS DE COLOMBIA")
    print("=" * 60)


def solicitar_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        print("Este campo es obligatorio.")
        texto = input(mensaje).strip()
    return texto


def solicitar_entero_positivo(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("Debe ingresar un número entero mayor que cero.")


def solicitar_consulta():
    print()
    return {
        "departamento": solicitar_texto("Departamento: "),
        "municipio": solicitar_texto("Municipio: "),
        "cultivo": solicitar_texto("Cultivo: "),
        "cantidad_registros": solicitar_entero_positivo("Número de registros a consultar: "),
    }


def formatear_mediana(valor_mediana):
    if valor_mediana is None:
        return TEXTO_SIN_DATOS
    return round(valor_mediana, 2)


def construir_fila_medianas(medianas):
    fila = []
    for nombre_variable in medianas:
        fila.append(formatear_mediana(medianas[nombre_variable]))
    return fila


def construir_encabezados_medianas(medianas):
    encabezados = []
    for nombre_variable in medianas:
        encabezados.append("Mediana " + nombre_variable)
    return encabezados


def mostrar_tabla_registros(resumen_registros):
    print()
    print("Registros encontrados: " + str(len(resumen_registros)))
    print(tabulate(resumen_registros, headers=ENCABEZADOS_REGISTROS, tablefmt="grid", showindex=range(1, len(resumen_registros) + 1)))


def mostrar_tabla_medianas(medianas):
    print()
    print("Mediana de las variables edáficas del cultivo consultado:")
    encabezados = construir_encabezados_medianas(medianas)
    fila = construir_fila_medianas(medianas)
    print(tabulate([fila], headers=encabezados, tablefmt="grid"))


def mostrar_resultados(resumen_registros, medianas):
    mostrar_tabla_registros(resumen_registros)
    mostrar_tabla_medianas(medianas)


def mostrar_sin_resultados(consulta):
    print()
    print(
        "No se encontraron registros para el cultivo " + consulta["cultivo"]
        + " en " + consulta["municipio"] + " (" + consulta["departamento"] + ")."
    )


def mostrar_error_archivo(ruta_archivo):
    print("No se encontró el archivo de datos: " + ruta_archivo)
    print("Verifique que el archivo esté en la carpeta del proyecto.")


def desea_realizar_otra_consulta():
    print()
    respuesta = input("¿Desea realizar otra consulta? (s/n): ").strip().lower()
    return respuesta == "s"


def mostrar_despedida():
    print()
    print("Gracias por usar la aplicación.")
