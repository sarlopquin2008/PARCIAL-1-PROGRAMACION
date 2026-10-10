from api.datos import (
    cargar_registros,
    filtrar_registros,
    construir_resumen_registros,
    calcular_medianas_edaficas,
)
from ui.interfaz import (
    mostrar_titulo,
    solicitar_consulta,
    mostrar_resultados,
    mostrar_sin_resultados,
    mostrar_error_archivo,
    desea_realizar_otra_consulta,
    mostrar_despedida,
)

RUTA_ARCHIVO_DATOS = "resultado_laboratorio_suelo.csv"


def atender_consulta(registros):
    consulta = solicitar_consulta()
    registros_encontrados = filtrar_registros(
        registros,
        consulta["departamento"],
        consulta["municipio"],
        consulta["cultivo"],
        consulta["cantidad_registros"],
    )
    if len(registros_encontrados) == 0:
        mostrar_sin_resultados(consulta)
        return
    resumen_registros = construir_resumen_registros(registros_encontrados)
    medianas = calcular_medianas_edaficas(registros_encontrados)
    mostrar_resultados(resumen_registros, medianas)


def main():
    mostrar_titulo()
    try:
        registros = cargar_registros(RUTA_ARCHIVO_DATOS)
    except FileNotFoundError:
        mostrar_error_archivo(RUTA_ARCHIVO_DATOS)
        return
    continuar = True
    while continuar:
        atender_consulta(registros)
        continuar = desea_realizar_otra_consulta()
    mostrar_despedida()


if __name__ == "__main__":
    main()
