"""Creación del navegador. La usan pytest (conftest.py) y Behave (features/environment.py)."""
import os

from selenium import webdriver


def crear_driver():
    """Abre Chrome listo para las pruebas y lo devuelve.

    Con la variable de entorno HEADLESS=1 corre sin abrir la ventana.
    No usa implicitly_wait: los Page Objects usan solo esperas explícitas.
    """
    opciones = webdriver.ChromeOptions()
    opciones.add_argument('--window-size=1366,900')
    # Evita el aviso de "contraseña filtrada" de Chrome, que tapa la página
    opciones.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.password_manager_leak_detection': False,
    })
    if os.environ.get('HEADLESS') == '1':
        opciones.add_argument('--headless=new')
    if os.environ.get('CI'):
        # GitHub Actions define CI=true. En esas máquinas Linux Chrome necesita estas dos opciones
        opciones.add_argument('--no-sandbox')
        opciones.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=opciones)
