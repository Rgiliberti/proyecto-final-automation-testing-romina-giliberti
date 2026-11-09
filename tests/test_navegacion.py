"""Navegación dentro de la tienda: detalle de producto, orden de la lista y logout."""
import pytest

from pages.login_page import LoginPage
from utils.datos import leer_json

PRODUCTOS = leer_json('productos.json')


@pytest.mark.parametrize('producto', PRODUCTOS[:2], ids=[p['nombre'] for p in PRODUCTOS[:2]])
def test_detalle_de_producto(usuario_logueado, producto):
    """El detalle muestra el mismo nombre y precio que la lista, y se puede volver."""
    inventario = usuario_logueado
    detalle = inventario.abrir_detalle(producto['nombre'])

    assert detalle == {'nombre': producto['nombre'], 'precio': producto['precio']}
    assert inventario.volver_a_productos().obtener_titulo() == 'Products'


def test_ordenar_por_precio_de_menor_a_mayor(usuario_logueado):
    precios = usuario_logueado.ordenar_por('Price (low to high)').obtener_precios()
    assert precios == sorted(precios), f'Los precios no quedaron ordenados: {precios}'


def test_cerrar_sesion(usuario_logueado, driver):
    usuario_logueado.cerrar_sesion()
    assert LoginPage(driver).esta_visible()
    # Después del logout no se puede volver al inventario escribiendo la URL
    driver.get('https://www.saucedemo.com/inventory.html')
    assert 'You can only access' in LoginPage(driver).obtener_mensaje_error()
