"""Configuración compartida por todos los tests (pytest carga este archivo solo).

- Fixtures `driver` y `usuario_logueado`: un navegador nuevo por test (tests independientes).
- Si un test de UI falla: captura en reports/screens/<test>_<fecha-hora>.png y adjunta al reporte.
- Resultado de cada test en logs/suite.log.
- Título, metadatos y columna URL del reporte HTML.
"""
import re
from datetime import datetime

import pytest
from pytest_metadata.plugin import metadata_key

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.driver import crear_driver
from utils.logger import CARPETA_PROYECTO, logger, ruta_relativa

CARPETA_CAPTURAS = CARPETA_PROYECTO / 'reports' / 'screens'
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


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Se ejecuta al terminar cada fase de un test. Si falló el cuerpo del test (fase
    'call') y usaba navegador, guarda la evidencia."""
    reporte = yield
    navegador = item.funcargs.get('driver')
    if reporte.when == 'call' and navegador is not None:
        reporte.url_pagina = navegador.current_url  # para la columna URL del reporte
        if reporte.failed:
            CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
            # Nombre: test + fecha y hora. Los parámetros traen [ ] y espacios: se cambian por _
            nombre = re.sub(r'[^\w-]+', '_', item.name).strip('_')
            momento = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            archivo = CARPETA_CAPTURAS / f'{nombre}_{momento}.png'
            navegador.save_screenshot(str(archivo))
            logger.error('Falló %s. Captura: %s', item.name, ruta_relativa(archivo))

            # La misma imagen dentro del reporte HTML (queda embebida, no depende del .png)
            pytest_html = item.config.pluginmanager.getplugin('html')
            if pytest_html is not None:
                extras = getattr(reporte, 'extras', [])
                extras.append(pytest_html.extras.image(navegador.get_screenshot_as_base64(), 'Captura'))
                reporte.extras = extras
    return reporte


def pytest_runtest_logreport(report):
    """Deja en el log el resultado de cada test (PASSED / FAILED / SKIPPED)."""
    if report.when == 'call' or (report.when == 'setup' and report.outcome != 'passed'):
        nivel = logger.error if report.failed else logger.info
        nivel('%s -> %s (%.2f s)', report.nodeid, report.outcome.upper(), report.duration)


# ---------- Personalización del reporte de pytest-html ----------

def pytest_html_report_title(report):
    report.title = 'Proyecto Final – Automation Testing (SauceDemo + JSONPlaceholder)'


def pytest_configure(config):
    """Metadatos que aparecen en la sección 'Environment' del reporte."""
    config.stash[metadata_key]['Proyecto'] = 'Proyecto final - Automation Testing'
    config.stash[metadata_key]['Autora'] = 'Romina Giliberti'


def pytest_html_results_table_header(cells):
    cells.insert(2, '<th>URL</th>')


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f'<td>{getattr(report, "url_pagina", "-")}</td>')
