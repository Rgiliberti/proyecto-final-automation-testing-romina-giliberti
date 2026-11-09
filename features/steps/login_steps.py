"""Steps de login.feature: cada frase en Gherkin llama a un método del Page Object."""
from behave import given, step_matcher, then, when

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.logger import logger


@given('que estoy en la página de login')
def abrir_login(context):
    logger.info('[BDD] Abro la página de login')
    context.login = LoginPage(context.driver).abrir()


# Matcher "re" (expresión regular) solo para este step: con el matcher común "{texto}"
# no acepta comillas vacías, y el Esquema tiene casos con usuario o clave vacíos.
step_matcher('re')


@when('ingreso el usuario "(?P<usuario>[^"]*)" y la clave "(?P<clave>[^"]*)"')
def ingresar_credenciales(context, usuario, clave):
    logger.info('[BDD] Ingreso usuario "%s"', usuario)
    context.login.login(usuario, clave)


step_matcher('parse')  # el resto de los steps vuelve al matcher común


@then('veo la página de productos con el título "{titulo}"')
def ver_productos(context, titulo):
    actual = InventoryPage(context.driver).esperar_carga().obtener_titulo()
    logger.info('[BDD] Título de la página: %s', actual)
    assert actual == titulo, f'Se esperaba el título "{titulo}" y apareció "{actual}"'


@then('la URL contiene "{fragmento}"')
def url_contiene(context, fragmento):
    logger.info('[BDD] URL actual: %s', context.driver.current_url)
    assert fragmento in context.driver.current_url


@then('veo el mensaje de error "{mensaje}"')
def ver_error(context, mensaje):
    actual = context.login.obtener_mensaje_error()
    assert actual == mensaje, f'Se esperaba "{mensaje}" y apareció "{actual}"'


@then('sigo en la página de login')
def sigo_en_login(context):
    logger.info('[BDD] Verifico que no pasó al inventario')
    assert '/inventory.html' not in context.driver.current_url
