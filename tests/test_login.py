"""Login parametrizado: cada fila de datos/login.csv es un test distinto.

Incluye casos positivos (3 usuarios que pueden entrar) y negativos
(bloqueado, clave incorrecta, usuario inexistente y campos vacíos).
"""
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.datos import leer_csv_login

CASOS_LOGIN = leer_csv_login('login.csv')


# ids: el nombre de cada caso en el reporte sale de la columna descripcion
@pytest.mark.parametrize('usuario, clave, debe_funcionar, descripcion', CASOS_LOGIN,
                         ids=[caso[3] for caso in CASOS_LOGIN])
def test_login_desde_csv(driver, usuario, clave, debe_funcionar, descripcion):
    login = LoginPage(driver).abrir().login(usuario, clave)

    if debe_funcionar:
        assert InventoryPage(driver).esperar_carga().obtener_titulo() == 'Products'
    else:
        # Caso negativo: aparece el cartel de error y no se pasa al inventario
        mensaje = login.obtener_mensaje_error()
        assert mensaje.startswith('Epic sadface'), f'Mensaje inesperado: {mensaje}'
        assert '/inventory.html' not in driver.current_url


@pytest.mark.smoke
def test_login_valido_smoke(usuario_logueado):
    """El fixture ya hizo login; alcanza con verificar que estamos en productos."""
    assert usuario_logueado.obtener_titulo() == 'Products'
