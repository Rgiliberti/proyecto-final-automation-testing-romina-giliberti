"""Lectura de los datos de prueba (CSV y JSON) de la carpeta datos/.

Los tests no tienen usuarios ni productos escritos a mano: si se agrega una fila
o un objeto en el archivo, aparece un test nuevo sin tocar código Python.
"""
import csv
import json
from pathlib import Path

# Carpeta datos/ del proyecto, sin importar desde dónde se ejecute pytest
CARPETA_DATOS = Path(__file__).resolve().parent.parent / 'datos'


def leer_csv_login(nombre_archivo):
    """Lee el CSV de credenciales.

    Retorna una lista de tuplas (usuario, clave, debe_funcionar, descripcion)
    lista para usar en pytest.mark.parametrize.
    """
    casos = []
    with open(CARPETA_DATOS / nombre_archivo, encoding='utf-8', newline='') as archivo:
        for fila in csv.DictReader(archivo):
            # En el CSV todo es texto: 'True' hay que pasarlo a booleano a mano
            debe_funcionar = fila['debe_funcionar'].strip().lower() == 'true'
            casos.append((fila['usuario'], fila['clave'], debe_funcionar, fila['descripcion']))
    return casos


def leer_json(nombre_archivo):
    """Lee un archivo JSON de datos/ y devuelve su contenido (en general, una lista)."""
    with open(CARPETA_DATOS / nombre_archivo, encoding='utf-8') as archivo:
        return json.load(archivo)
