"""Clase base de todos los Page Objects.

Tiene las esperas explícitas que usan todas las páginas, así cada Page Object
solo declara sus selectores y sus acciones.
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, tiempo=10):
        self.driver = driver
        self.espera = WebDriverWait(driver, tiempo)

    def _visible(self, selector, mensaje=''):
        """Espera a que el elemento se vea y lo devuelve."""
        return self.espera.until(EC.visibility_of_element_located(selector), mensaje)

    def _todos_visibles(self, selector, mensaje=''):
        return self.espera.until(EC.visibility_of_all_elements_located(selector), mensaje)

    def _clic(self, selector, mensaje=''):
        self.espera.until(EC.element_to_be_clickable(selector), mensaje).click()

    def _escribir(self, selector, texto):
        campo = self._visible(selector)
        campo.clear()
        campo.send_keys(texto)

    def _esperar_url(self, fragmento):
        self.espera.until(EC.url_contains(fragmento), f'La URL no llegó a contener "{fragmento}"')

    @staticmethod
    def _a_numero(texto):
        """'$29.99' o 'Total: $43.18' -> 29.99 / 43.18"""
        return float(texto.split('$')[-1])
