"""Steps de cart.feature."""
from behave import given, then, when

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.logger import logger

CLAVE = 'secret_sauce'  # clave pública de los usuarios de prueba de SauceDemo


@given('que inicié sesión con el usuario "{usuario}"')
def iniciar_sesion(context, usuario):
    logger.info('[BDD] Login automático con %s', usuario)
    LoginPage(context.driver).abrir().login(usuario, CLAVE)
    context.inventario = InventoryPage(context.driver).esperar_carga()


@when('agrego el producto "{producto}" al carrito')
def agregar_producto(context, producto):
    logger.info('[BDD] Agrego "%s"', producto)
    context.inventario.agregar_producto_por_nombre(producto)


@when('agrego estos productos al carrito:')
def agregar_varios(context):
    # context.table es la tabla que viene debajo del step en el .feature
    for fila in context.table:
        logger.info('[BDD] Agrego "%s"', fila['producto'])
        context.inventario.agregar_producto_por_nombre(fila['producto'])


@then('el contador del carrito muestra "{cantidad:d}"')
def ver_contador(context, cantidad):
    actual = context.inventario.obtener_contador_carrito()
    logger.info('[BDD] Contador del carrito: %s', actual)
    assert actual == cantidad, f'El carrito muestra {actual} y se esperaba {cantidad}'


@then('el carrito contiene "{producto}"')
def carrito_contiene(context, producto):
    productos = context.inventario.ir_al_carrito().obtener_nombres()
    assert producto in productos, f'"{producto}" no está en el carrito: {productos}'
