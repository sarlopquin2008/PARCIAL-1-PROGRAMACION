import unicodedata

import pandas as pd

COLUMNA_DEPARTAMENTO = "Departamento"
COLUMNA_MUNICIPIO = "Municipio"
COLUMNA_CULTIVO = "Cultivo"
COLUMNA_TOPOGRAFIA = "Topografia"

INICIO_NOMBRE_COLUMNAS_EDAFICAS = {
    "pH": "pH",
    "Fósforo (P)": "Fósforo",
    "Potasio (K)": "Potasio",
}


def cargar_registros(ruta_archivo):
    tabla = leer_tabla(ruta_archivo)
    tabla = tabla.fillna("")
    return tabla.to_dict("records")


def leer_tabla(ruta_archivo):
    if ruta_archivo.lower().endswith(".csv"):
        return pd.read_csv(ruta_archivo, dtype=str)
    return pd.read_excel(ruta_archivo, dtype=str)


def normalizar_texto(texto):
    texto_descompuesto = unicodedata.normalize("NFD", str(texto))
    caracteres_sin_tilde = []
    for caracter in texto_descompuesto:
        if unicodedata.category(caracter) != "Mn":
            caracteres_sin_tilde.append(caracter)
    return "".join(caracteres_sin_tilde).strip().upper()


def textos_coinciden(texto_registro, texto_buscado):
    return normalizar_texto(texto_registro) == normalizar_texto(texto_buscado)


def es_registro_buscado(registro, departamento, municipio, cultivo):
    return (
        textos_coinciden(registro[COLUMNA_DEPARTAMENTO], departamento)
        and textos_coinciden(registro[COLUMNA_MUNICIPIO], municipio)
        and textos_coinciden(registro[COLUMNA_CULTIVO], cultivo)
    )


def filtrar_registros(registros, departamento, municipio, cultivo, cantidad_maxima):
    registros_encontrados = []
    for registro in registros:
        if len(registros_encontrados) == cantidad_maxima:
            break
        if es_registro_buscado(registro, departamento, municipio, cultivo):
            registros_encontrados.append(registro)
    return registros_encontrados


def obtener_datos_generales(registro):
    return [
        registro[COLUMNA_DEPARTAMENTO],
        registro[COLUMNA_MUNICIPIO],
        registro[COLUMNA_CULTIVO],
        registro[COLUMNA_TOPOGRAFIA],
    ]


def construir_resumen_registros(registros):
    resumen = []
    for registro in registros:
        resumen.append(obtener_datos_generales(registro))
    return resumen


def buscar_columna_que_inicia_con(registro, inicio_nombre):
    for nombre_columna in registro:
        if normalizar_texto(nombre_columna).startswith(normalizar_texto(inicio_nombre)):
            return nombre_columna
    raise KeyError("No existe una columna que inicie con: " + inicio_nombre)


def convertir_a_numero(valor):
    texto = str(valor).strip().replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def extraer_valores_numericos(registros, nombre_columna):
    valores = []
    for registro in registros:
        numero = convertir_a_numero(registro[nombre_columna])
        if numero is not None:
            valores.append(numero)
    return valores


def calcular_mediana(valores):
    if len(valores) == 0:
        return None
    valores_ordenados = sorted(valores)
    posicion_central = len(valores_ordenados) // 2
    if len(valores_ordenados) % 2 == 1:
        return valores_ordenados[posicion_central]
    return (valores_ordenados[posicion_central - 1] + valores_ordenados[posicion_central]) / 2


def calcular_medianas_edaficas(registros):
    medianas = {}
    for nombre_variable, inicio_nombre_columna in INICIO_NOMBRE_COLUMNAS_EDAFICAS.items():
        nombre_columna = buscar_columna_que_inicia_con(registros[0], inicio_nombre_columna)
        valores = extraer_valores_numericos(registros, nombre_columna)
        medianas[nombre_variable] = calcular_mediana(valores)
    return medianas
