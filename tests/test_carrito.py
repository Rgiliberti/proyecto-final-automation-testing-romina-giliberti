"""Carrito: un test por cada producto de datos/productos.json, más quitar y smoke."""
import pytest

from utils.datos import leer_json

PRODUCTOS = leer_json('productos.json')


@pytest.mark.parametrize('producto', PRODUCTOS, ids=[p['nombre'] for p in PRODUCTOS])
def test_agregar_producto_desde_json(usuario_logueado, producto):
    inventario = usuario_logueado
    # El precio de la página tiene que coincidir con el del JSON
    assert inventario.obtener_precio(producto['nombre']) == producto['precio']

    inventario.agregar_producto_por_nombre(producto['nombre'])
    assert inventario.obtener_contador_carrito() == 1
    assert inventario.ir_al_carrito().obtener_nombres() == [producto['nombre']]


def test_quitar_producto_del_carrito(usuario_logueado):
    inventario = usuario_logueado
    inventario.agregar_producto_por_nombre(PRODUCTOS[0]['nombre'])
    inventario.agregar_producto_por_nombre(PRODUCTOS[1]['nombre'])

    carrito = inventario.ir_al_carrito().quitar_producto(PRODUCTOS[0]['nombre'])
    assert carrito.obtener_nombres() == [PRODUCTOS[1]['nombre']]


@pytest.mark.smoke
def test_carrito_smoke(usuario_logueado):
    inventario = usuario_logueado
    assert inventario.obtener_contador_carrito() == 0  # arranca vacío

    nombre = inventario.agregar_primer_producto()
    assert inventario.obtener_contador_carrito() == 1
    assert inventario.ir_al_carrito().obtener_nombres() == [nombre]
