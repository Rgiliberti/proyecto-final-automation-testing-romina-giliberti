"""Page Object de la pantalla de login de SauceDemo."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import logger


class LoginPage(BasePage):
    URL = 'https://www.saucedemo.com/'

    # Selectores (regla de oro: ID -> NAME -> CSS -> XPath)
    _CAMPO_USUARIO = (By.ID, 'user-name')
    _CAMPO_CLAVE = (By.NAME, 'password')
    _BOTON_LOGIN = (By.ID, 'login-button')
    _MENSAJE_ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def abrir(self):
        """Abre la página de login y espera a que aparezca el campo usuario."""
        logger.info('Abriendo %s', self.URL)
        self.driver.get(self.URL)
        self._visible(self._CAMPO_USUARIO)
        return self

    def login(self, usuario, clave):
        """Completa usuario y clave y presiona Login (no verifica el resultado)."""
        logger.info('Login con usuario "%s"', usuario)  # la clave no se escribe en el log
        self._escribir(self._CAMPO_USUARIO, usuario)
        self._escribir(self._CAMPO_CLAVE, clave)
        self._clic(self._BOTON_LOGIN)
        return self

    def obtener_mensaje_error(self):
        """Espera el cartel rojo de error y devuelve su texto."""
        mensaje = self._visible(self._MENSAJE_ERROR, 'No apareció el mensaje de error').text
        logger.info('Mensaje de error en pantalla: %s', mensaje)
        return mensaje

    def esta_visible(self):
        """True si se ve el botón de Login (o sea, estamos en la pantalla de login)."""
        return self._visible(self._BOTON_LOGIN).is_displayed()
