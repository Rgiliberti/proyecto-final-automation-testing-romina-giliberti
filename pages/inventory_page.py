"""Page Object de la página de productos (inventario) de SauceDemo.

Incluye lo que se usa desde esta página: el carrito del encabezado, el menú
lateral (cerrar sesión), el orden de la lista y el detalle de un producto.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from pages.cart_page import CartPage
from utils.logger import logger


class InventoryPage(BasePage):
    _TITULO = (By.CSS_SELECTOR, '[data-test="title"]')
    _PRODUCTOS = (By.CSS_SELECTOR, '.inventory_item')
    _NOMBRES = (By.CSS_SELECTOR, '.inventory_item_name')
    _PRECIOS = (By.CSS_SELECTOR, '.inventory_item_price')
    _ORDEN = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    _ICONO_CARRITO = (By.CSS_SELECTOR, '.shopping_cart_link')
    _CONTADOR_CARRITO = (By.CSS_SELECTOR, '.shopping_cart_badge')
    _BOTON_MENU = (By.ID, 'react-burger-menu-btn')
    _CERRAR_SESION = (By.ID, 'logout_sidebar_link')
    # Página de detalle de un producto
    _DETALLE_NOMBRE = (By.CSS_SELECTOR, '.inventory_details_name')
    _DETALLE_PRECIO = (By.CSS_SELECTOR, '.inventory_details_price')
    _VOLVER = (By.ID, 'back-to-products')

    def esperar_carga(self):
        """Espera a estar en /inventory.html con el título visible."""
        self._esperar_url('/inventory.html')
        self._visible(self._TITULO)
        return self

    def obtener_titulo(self):
        return self._visible(self._TITULO).text

    @staticmethod
    def _tarjeta(nombre):
        """Selector XPath de la tarjeta (el recuadro) del producto con ese nombre."""
        return f'//div[@class="inventory_item"][.//div[normalize-space()="{nombre}"]]'

    def obtener_precio(self, nombre):
        """Precio que muestra la lista para ese producto, como número (ej. 29.99)."""
        precio = (By.XPATH, self._tarjeta(nombre) + '//div[@class="inventory_item_price"]')
        return self._a_numero(self._visible(precio, f'No se encontró el producto "{nombre}"').text)

    def obtener_precios(self):
        """Precios de todos los productos, en el orden en que aparecen."""
        return [self._a_numero(e.text) for e in self._todos_visibles(self._PRECIOS)]

    def agregar_producto_por_nombre(self, nombre):
        """Clic en 'Add to cart' del producto y espera a que el botón pase a 'Remove'."""
        logger.info('Agregando al carrito: %s', nombre)
        boton = (By.XPATH, self._tarjeta(nombre) + '//button')
        self._clic(boton, f'No se encontró el producto "{nombre}"')
        # La página reemplaza el botón por otro nuevo ("Remove"): se vuelve a buscar
        # con el selector para no usar el elemento viejo (StaleElementReferenceException)
        self.espera.until(EC.text_to_be_present_in_element(boton, 'Remove'),
                          f'"{nombre}" no se agregó al carrito')
        return self

    def agregar_primer_producto(self):
        """Agrega el primer producto de la lista y devuelve su nombre."""
        nombre = self._todos_visibles(self._NOMBRES)[0].text
        self.agregar_producto_por_nombre(nombre)
        return nombre

    def obtener_contador_carrito(self):
        """Número del globito del carrito; 0 si no hay globito (carrito vacío)."""
        globitos = self.driver.find_elements(*self._CONTADOR_CARRITO)
        return int(globitos[0].text) if globitos else 0

    def ir_al_carrito(self):
        logger.info('Abriendo el carrito')
        self._clic(self._ICONO_CARRITO)
        return CartPage(self.driver).esperar_carga()

    def ordenar_por(self, texto_opcion):
        """Elige una opción del desplegable de orden, por el texto que se ve."""
        logger.info('Ordenando productos por "%s"', texto_opcion)
        Select(self._visible(self._ORDEN)).select_by_visible_text(texto_opcion)
        return self

    def abrir_detalle(self, nombre):
        """Clic en el nombre del producto. Devuelve nombre y precio que muestra el detalle."""
        logger.info('Abriendo el detalle de %s', nombre)
        self._clic((By.XPATH, f'//div[contains(@class, "inventory_item_name")][normalize-space()="{nombre}"]'))
        self._esperar_url('/inventory-item.html')
        return {'nombre': self._visible(self._DETALLE_NOMBRE).text,
                'precio': self._a_numero(self._visible(self._DETALLE_PRECIO).text)}

    def volver_a_productos(self):
        self._clic(self._VOLVER)
        return self.esperar_carga()

    def cerrar_sesion(self):
        """Abre el menú lateral y hace clic en Logout."""
        logger.info('Cerrando sesión desde el menú')
        self._clic(self._BOTON_MENU)
        self._clic(self._CERRAR_SESION)  # espera a que termine la animación del menú
        self._esperar_url('saucedemo.com/')
        return self
