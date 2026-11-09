"""Checkout: la compra completa de punta a punta y los errores del formulario."""
import pytest
from faker import Faker

from utils.datos import leer_json

PRODUCTOS = leer_json('productos.json')
CASOS_INCOMPLETOS = leer_json('checkout_incompleto.json')
TASA_IMPUESTO = 0.08  # SauceDemo cobra 8 % de impuesto sobre el subtotal

fake = Faker('es_AR')


@pytest.mark.smoke
@pytest.mark.e2e
def test_compra_completa(usuario_logueado):
    """Login -> agregar 2 productos -> carrito -> datos de envío -> resumen -> finalizar."""
    comprados = PRODUCTOS[:2]
    inventario = usuario_logueado
    for producto in comprados:
        inventario.agregar_producto_por_nombre(producto['nombre'])

    carrito = inventario.ir_al_carrito()
    assert carrito.obtener_nombres() == [p['nombre'] for p in comprados]

    checkout = carrito.ir_al_checkout()
    checkout.completar_datos(fake.first_name(), fake.last_name(), fake.postcode())

    # El resumen tiene que cerrar: precios del JSON, subtotal, 8 % de impuesto y total
    resumen = checkout.obtener_resumen()
    subtotal = round(sum(p['precio'] for p in comprados), 2)
    assert resumen['precios'] == [p['precio'] for p in comprados]
    assert resumen['subtotal'] == subtotal
    assert resumen['impuesto'] == round(subtotal * TASA_IMPUESTO, 2)
    assert resumen['total'] == round(resumen['subtotal'] + resumen['impuesto'], 2)

    assert checkout.finalizar() == 'Thank you for your order!'


@pytest.mark.parametrize('caso', CASOS_INCOMPLETOS, ids=[c['caso'] for c in CASOS_INCOMPLETOS])
def test_checkout_con_datos_incompletos(usuario_logueado, caso):
    """Caso negativo: si falta un dato, el formulario muestra el error y no avanza."""
    usuario_logueado.agregar_primer_producto()
    checkout = usuario_logueado.ir_al_carrito().ir_al_checkout()

    checkout.completar_datos(caso['nombre'], caso['apellido'], caso['codigo_postal'])
    assert checkout.obtener_mensaje_error() == caso['error']
    assert '/checkout-step-one.html' in checkout.driver.current_url
