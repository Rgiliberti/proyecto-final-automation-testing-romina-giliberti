# language: es
@ui
Característica: Login en SauceDemo
  Como cliente de la tienda
  Quiero ingresar con mi usuario y contraseña
  Para poder ver los productos

  Antecedentes:
    Dado que estoy en la página de login

  @smoke
  Escenario: Login exitoso con el usuario estándar
    Cuando ingreso el usuario "standard_user" y la clave "secret_sauce"
    Entonces veo la página de productos con el título "Products"
    Y la URL contiene "inventory.html"

  Esquema del escenario: Login fallido por <caso>
    Cuando ingreso el usuario "<usuario>" y la clave "<clave>"
    Entonces veo el mensaje de error "<mensaje>"
    Y sigo en la página de login

    Ejemplos:
      | caso              | usuario         | clave        | mensaje                                                                    |
      | clave incorrecta  | standard_user   | clave_mala   | Epic sadface: Username and password do not match any user in this service |
      | usuario bloqueado | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | usuario vacío     |                 | secret_sauce | Epic sadface: Username is required                                        |
      | clave vacía       | standard_user   |              | Epic sadface: Password is required                                        |
