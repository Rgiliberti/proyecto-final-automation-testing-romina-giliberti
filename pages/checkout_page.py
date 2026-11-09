"""Page Object del checkout: los tres pasos de la compra.

1. /checkout-step-one.html  -> formulario con nombre, apellido y código postal
2. /checkout-step-two.html  -> resumen con subtotal, impuesto y total
3. /checkout-complete.html  -> mensaje de compra terminada
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import logger


class CheckoutPage(BasePage):
    # Paso 1
    _NOMBRE = (By.ID, 'first-name')
    _APELLIDO = (By.ID, 'last-name')
    _CODIGO_POSTAL = (By.ID, 'postal-code')
    _CONTINUAR = (By.ID, 'continue')
    _MENSAJE_ERROR = (By.CSS_SELECTOR, '[data-test="error"]')
    # Paso 2
    _PRECIOS_ITEMS = (By.CSS_SELECTOR, '.cart_item .inventory_item_price')
    _SUBTOTAL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    _IMPUESTO = (By.CSS_SELECTOR, '[data-test="tax-label"]')
    _TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    _FINALIZAR = (By.ID, 'finish')
    # Paso 3
    _MENSAJE_FINAL = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def esperar_formulario(self):
        self._esperar_url('/checkout-step-one.html')
        self._visible(self._NOMBRE)
        return self

    def completar_datos(self, nombre, apellido, codigo_postal):
        """Completa el formulario del paso 1 y presiona Continue (no verifica el resultado)."""
        logger.info('Datos de envío: "%s" "%s" "%s"', nombre, apellido, codigo_postal)
        self._escribir(self._NOMBRE, nombre)
        self._escribir(self._APELLIDO, apellido)
        self._escribir(self._CODIGO_POSTAL, codigo_postal)
        self._clic(self._CONTINUAR)
        return self

    def obtener_mensaje_error(self):
        mensaje = self._visible(self._MENSAJE_ERROR, 'No apareció el mensaje de error').text
        logger.info('Mensaje de error en el checkout: %s', mensaje)
        return mensaje

    def obtener_resumen(self):
        """Lee el paso 2. Devuelve los precios de cada producto y los importes como números."""
        self._esperar_url('/checkout-step-two.html')
        resumen = {
            'precios': [self._a_numero(e.text) for e in self._todos_visibles(self._PRECIOS_ITEMS)],
            'subtotal': self._a_numero(self._visible(self._SUBTOTAL).text),
            'impuesto': self._a_numero(self._visible(self._IMPUESTO).text),
            'total': self._a_numero(self._visible(self._TOTAL).text),
        }
        logger.info('Resumen de la compra: %s', resumen)
        return resumen

    def finalizar(self):
        """Presiona Finish y devuelve el mensaje de la pantalla final."""
        self._clic(self._FINALIZAR)
        self._esperar_url('/checkout-complete.html')
        mensaje = self._visible(self._MENSAJE_FINAL).text
        logger.info('Compra terminada: %s', mensaje)
        return mensaje
