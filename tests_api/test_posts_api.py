"""Pruebas de API sobre el recurso /posts de JSONPlaceholder.

Cubre GET, POST y DELETE (y PATCH en el flujo encadenado), con escenarios
de éxito y de error. Se valida código de estado, estructura del JSON,
tipos de dato, contenido y tiempo de respuesta.
"""
import pytest

from utils.api_client import pedir, validar_esquema, validar_respuesta
from utils.datos import leer_json
from utils.logger import logger

# Todos los tests de este archivo llevan el marker api
pytestmark = pytest.mark.api

POSTS_NUEVOS = leer_json('posts_nuevos.json')


@pytest.mark.smoke
def test_obtener_post_por_id():
    post = validar_respuesta(pedir('GET', '/posts/1'), 200)
    validar_esquema(post)
    assert post['id'] == 1
    assert post['title'].strip() != ''


def test_listar_posts_de_un_usuario():
    """GET con parámetro: ?userId=1 devuelve solo los posts de ese usuario."""
    posts = validar_respuesta(pedir('GET', '/posts', params={'userId': 1}), 200)
    assert isinstance(posts, list) and len(posts) == 10
    for post in posts:
        validar_esquema(post)
        assert post['userId'] == 1


def test_post_inexistente_devuelve_404():
    """Escenario de error: un id que no existe responde 404 con un JSON vacío."""
    respuesta = validar_respuesta(pedir('GET', '/posts/99999'), 404)
    assert respuesta == {}


@pytest.mark.parametrize('nuevo', POSTS_NUEVOS, ids=[f"userId {p['userId']}" for p in POSTS_NUEVOS])
def test_crear_post(nuevo):
    """POST con datos de datos/posts_nuevos.json: responde 201 y devuelve lo enviado con un id."""
    creado = validar_respuesta(pedir('POST', '/posts', json=nuevo), 201)
    validar_esquema(creado)
    for clave in ('title', 'body', 'userId'):
        assert creado[clave] == nuevo[clave]


def test_eliminar_post():
    borrado = validar_respuesta(pedir('DELETE', '/posts/1'), 200)
    assert borrado == {}


@pytest.mark.e2e
# Si falla por un problema de red, pytest-rerunfailures lo reintenta 2 veces (3 s entre cada una)
@pytest.mark.flaky(reruns=2, reruns_delay=3)
def test_ciclo_de_vida_post():
    """Flujo encadenado: POST crea, PATCH cambia el título y DELETE borra,
    usando en cada paso el id que devolvió el POST."""
    creado = validar_respuesta(pedir('POST', '/posts', json=POSTS_NUEVOS[0]), 201)
    post_id = creado['id']
    logger.info('Post creado con id %s', post_id)

    actualizado = validar_respuesta(
        pedir('PATCH', f'/posts/{post_id}', json={'title': 'Título actualizado por QA'}), 200)
    assert actualizado['title'] == 'Título actualizado por QA'

    assert validar_respuesta(pedir('DELETE', f'/posts/{post_id}'), 200) == {}
