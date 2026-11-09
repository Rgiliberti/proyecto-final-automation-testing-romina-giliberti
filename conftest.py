"""Configuración compartida por todos los tests (pytest carga este archivo solo).

- Fixtures `driver` y `usuario_logueado`: un navegador nuevo por test (tests independientes).
"""
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.driver import crear_driver
from utils.logger import logger

USUARIO = 'standard_user'
CLAVE = 'secret_sauce'  # clave pública de los usuarios de prueba de SauceDemo


@pytest.fixture
def driver(request):
    """Abre Chrome antes de cada test y lo cierra después, pase lo que pase."""
    navegador = crear_driver()
    logger.info('Inicio de %s: navegador abierto', request.node.name)
    yield navegador
    # Teardown: se ejecuta después del test aunque haya fallado
    navegador.quit()
    logger.info('Fin de %s: navegador cerrado', request.node.name)


@pytest.fixture
def usuario_logueado(driver):
    """Hace login con el usuario estándar y entrega la página de productos."""
    LoginPage(driver).abrir().login(USUARIO, CLAVE)
    return InventoryPage(driver).esperar_carga()
