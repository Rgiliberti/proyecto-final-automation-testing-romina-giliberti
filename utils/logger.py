"""Logger del proyecto: todo lo que pasa en la suite queda en logs/suite.log.

Uso en cualquier archivo:
    from utils.logger import logger
    logger.info('Login con usuario %s', usuario)

Niveles: DEBUG < INFO < WARNING < ERROR < CRITICAL. Se guarda de INFO para arriba.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_LOGS = CARPETA_PROYECTO / 'logs'
ARCHIVO_LOG = CARPETA_LOGS / 'suite.log'
FORMATO = '%(asctime)s %(levelname)s %(name)s – %(message)s'


def _crear_logger():
    CARPETA_LOGS.mkdir(exist_ok=True)
    log = logging.getLogger('talentolab')
    log.setLevel(logging.INFO)
    # pytest importa este archivo una sola vez, pero por las dudas no se duplica el handler
    if not log.handlers:
        # RotatingFileHandler: cuando el archivo llega a 1 MB lo renombra a suite.log.1
        # y empieza uno nuevo (guarda hasta 3 viejos). Así el log no crece para siempre.
        archivo = RotatingFileHandler(ARCHIVO_LOG, maxBytes=1_000_000, backupCount=3, encoding='utf-8')
        archivo.setFormatter(logging.Formatter(FORMATO))
        log.addHandler(archivo)
    return log


logger = _crear_logger()


def ruta_relativa(ruta):
    """Ruta desde la carpeta del proyecto, para no escribir datos de la máquina en el log."""
    return Path(ruta).resolve().relative_to(CARPETA_PROYECTO).as_posix()
