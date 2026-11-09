"""Page Object del carrito (/cart.html)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage
from utils.logger import logger


class CartPage(BasePage):
    _BOTON_CHECKOUT = (By.ID, 'checkout')
    _ITEMS = (By.CSS_SELECTOR, '.cart_item')
    _NOMBRES = (By.CSS_SELECTOR, '.cart_item .inventory_item_name')

    def esperar_carga(self):
        # El botón Checkout se dibuja junto con la lista: cuando se ve, la lista ya está
        self._esperar_url('/cart.html')
        self._visible(self._BOTON_CHECKOUT)
        return self

    def obtener_nombres(self):
        """Nombres de los productos que hay en el carrito (lista vacía si no hay)."""
        nombres = [e.text for e in self.driver.find_elements(*self._NOMBRES)]
        logger.info('Productos en el carrito: %s', nombres)
        return nombres

    def quitar_producto(self, nombre):
        """Clic en 'Remove' del producto y espera a que desaparezca de la lista."""
        logger.info('Quitando del carrito: %s', nombre)
        item = (By.XPATH, f'//div[@class="cart_item"][.//div[normalize-space()="{nombre}"]]')
        self._clic((By.XPATH, item[1] + '//button'))
        self.espera.until(lambda d: not d.find_elements(*item), f'"{nombre}" sigue en el carrito')
        return self

    def ir_al_checkout(self):
        logger.info('Yendo al checkout')
        self._clic(self._BOTON_CHECKOUT)
        return CheckoutPage(self.driver).esperar_formulario()
