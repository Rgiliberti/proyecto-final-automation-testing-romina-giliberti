# language: es
@ui @regression
Característica: Carrito de compras
  Como cliente que ya inició sesión
  Quiero agregar productos al carrito
  Para después poder comprarlos

  Antecedentes:
    Dado que inicié sesión con el usuario "standard_user"

  Escenario: Agregar la mochila al carrito
    Cuando agrego el producto "Sauce Labs Backpack" al carrito
    Entonces el contador del carrito muestra "1"
    Y el carrito contiene "Sauce Labs Backpack"

  Escenario: Agregar varios productos al carrito
    Cuando agrego estos productos al carrito:
      | producto                |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Entonces el contador del carrito muestra "3"
