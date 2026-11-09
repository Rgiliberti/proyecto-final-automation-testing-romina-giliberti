"""Herramientas para las pruebas de API contra JSONPlaceholder.

JSONPlaceholder (https://jsonplaceholder.typicode.com) es una API REST de práctica:
acepta GET, POST, PUT, PATCH y DELETE, no pide clave y no tiene límite diario.
Responde como si guardara los cambios, pero no guarda nada.
"""
import requests

from utils.logger import logger

BASE_URL = 'https://jsonplaceholder.typicode.com'
TIMEOUT = 10          # segundos que espera requests antes de cortar la conexión
TIEMPO_MAXIMO = 3.0   # segundos aceptables para que responda la API

# Estructura esperada de un post: cada campo con su tipo de dato
ESQUEMA_POST = {'userId': int, 'id': int, 'title': str, 'body': str}


def pedir(metodo, ruta, **kwargs):
    """Hace el pedido HTTP y lo deja en el log. Ejemplo: pedir('GET', '/posts/1')."""
    respuesta = requests.request(metodo, BASE_URL + ruta, timeout=TIMEOUT, **kwargs)
    logger.info('%s %s -> %s (%.2f s)', metodo, ruta, respuesta.status_code,
                respuesta.elapsed.total_seconds())
    return respuesta


def validar_respuesta(respuesta, codigo_esperado, tiempo_maximo=TIEMPO_MAXIMO):
    """Validaciones que se repiten en todos los tests de API. Devuelve el JSON.

    1. Código de estado esperado.
    2. Header Content-Type: la respuesta tiene que ser JSON.
    3. Tiempo de respuesta por debajo del máximo.
    """
    assert respuesta.status_code == codigo_esperado, (
        f'Se esperaba {codigo_esperado} y llegó {respuesta.status_code}: {respuesta.text[:200]}')
    assert 'application/json' in respuesta.headers.get('Content-Type', '')
    segundos = respuesta.elapsed.total_seconds()
    assert segundos < tiempo_maximo, f'La API tardó {segundos:.2f} s (máximo {tiempo_maximo} s)'
    return respuesta.json()


def validar_esquema(dato, esquema=ESQUEMA_POST):
    """Revisa que el diccionario tenga todas las claves del esquema con el tipo correcto."""
    for clave, tipo in esquema.items():
        assert clave in dato, f'Falta la clave "{clave}" en {dato}'
        assert isinstance(dato[clave], tipo), (
            f'"{clave}" debería ser {tipo.__name__} y es {type(dato[clave]).__name__}')
