"""Hooks de Behave: el equivalente a conftest.py de pytest.

Behave los llama solo, en este orden:
before_all -> (before_scenario -> pasos -> after_step por cada paso) x escenario -> after_all
"""
import re
import sys
from datetime import datetime
from pathlib import Path

# Behave no agrega la carpeta del proyecto al path: sin esto no encuentra pages/ ni utils/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.driver import crear_driver  # noqa: E402
from utils.logger import CARPETA_PROYECTO, logger, ruta_relativa  # noqa: E402

CARPETA_CAPTURAS = CARPETA_PROYECTO / 'reports' / 'screens'


def before_all(context):
    """Un solo navegador para toda la corrida (abrir uno por escenario tarda mucho más)."""
    context.driver = crear_driver()
    logger.info('[BDD] Navegador abierto')


def before_scenario(context, scenario):
    """Cada escenario arranca limpio: sin sesión y con el carrito vacío.
    SauceDemo guarda la sesión en una cookie y el carrito en el localStorage."""
    logger.info('[BDD] Iniciando escenario: %s', scenario.name)
    if context.driver.current_url.startswith('http'):
        context.driver.delete_all_cookies()
        context.driver.execute_script('window.localStorage.clear();')


def after_step(context, step):
    """Si un paso falla, guarda una captura con el nombre del escenario, del paso y la hora."""
    if step.status == 'failed':
        CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
        nombre = re.sub(r'[^\w-]+', '_', f'{context.scenario.name}_{step.name}').strip('_')[:120]
        momento = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        archivo = CARPETA_CAPTURAS / f'{nombre}_{momento}.png'
        context.driver.save_screenshot(str(archivo))
        logger.error('[BDD] Falló el paso "%s". Captura: %s', step.name, ruta_relativa(archivo))


def after_scenario(context, scenario):
    logger.info('[BDD] Escenario "%s" -> %s', scenario.name, scenario.status.name.upper())


def after_all(context):
    context.driver.quit()
    logger.info('[BDD] Navegador cerrado')
