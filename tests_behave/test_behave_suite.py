"""Corre la suite BDD (Behave) desde pytest, así `pytest` ejecuta todo junto.

Behave es otro programa: se lanza con subprocess.run() y se mira su código de salida
(0 = todos los escenarios pasaron). Cada test deja dos reportes:
- reports/behave_<tag>.json  -> para herramientas (CI, Jira, etc.)
- reports/behave_<tag>.html  -> para personas (Silvia, el cliente)
y la salida "pretty" queda en la sección "Captured stdout" del reporte de pytest.
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent


def correr_behave(tag):
    comando = [
        sys.executable, '-m', 'behave', '-t', tag,
        '-f', 'json', '-o', f'reports/behave_{tag[1:]}.json',
        '-f', 'html', '-o', f'reports/behave_{tag[1:]}.html',
        '-f', 'pretty',
    ]
    # PYTHONUTF8=1: que los acentos de los .feature salgan bien en la consola de Windows
    entorno = {**os.environ, 'PYTHONUTF8': '1'}
    resultado = subprocess.run(comando, cwd=CARPETA_PROYECTO, env=entorno,
                               capture_output=True, text=True, encoding='utf-8')
    print(resultado.stdout)
    return resultado


@pytest.mark.bdd
@pytest.mark.smoke
def test_bdd_smoke():
    resultado = correr_behave('@smoke')
    assert resultado.returncode == 0, f'Fallaron escenarios @smoke:\n{resultado.stdout[-1500:]}{resultado.stderr}'


@pytest.mark.bdd
@pytest.mark.regression
def test_bdd_regression():
    resultado = correr_behave('@regression')
    assert resultado.returncode == 0, f'Fallaron escenarios @regression:\n{resultado.stdout[-1500:]}{resultado.stderr}'
