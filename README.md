# Proyecto Final – Automation Testing

![CI](https://github.com/Rgiliberti/proyecto-final-automation-testing-romina-giliberti/actions/workflows/ci.yml/badge.svg)

Framework de pruebas automatizadas hecho como entrega final del curso de Automation Testing.
Prueba la interfaz de la tienda de demo [SauceDemo](https://www.saucedemo.com/) y la API REST de
[JSONPlaceholder](https://jsonplaceholder.typicode.com/), con reportes HTML, capturas de pantalla
cuando algo falla, log de ejecución, escenarios BDD y CI en GitHub Actions.

**Autora:** Romina Giliberti

## Tecnologías

| Herramienta | Para qué se usa |
|---|---|
| Python 3.12 | Lenguaje del proyecto |
| Pytest | Ejecuta los tests, fixtures, markers y parametrización |
| Selenium WebDriver | Maneja Chrome para las pruebas de UI |
| Requests | Pedidos HTTP para las pruebas de API |
| pytest-html | Reporte HTML con estado, duración y capturas |
| pytest-rerunfailures | Reintenta el test de API que depende de la red |
| Faker | Datos de envío aleatorios para el checkout |
| Behave | Escenarios BDD escritos en Gherkin (en español) |
| GitHub Actions | Corre todo en cada push y guarda los reportes |

## Estructura

```
├── .github/workflows/ci.yml    # pipeline de CI
├── pages/                      # Page Object Model: una clase por página
│   ├── base_page.py            #   esperas explícitas que usan todas las páginas
│   ├── login_page.py
│   ├── inventory_page.py       #   productos, orden, detalle, menú y carrito del encabezado
│   ├── cart_page.py
│   └── checkout_page.py        #   los 3 pasos de la compra
├── tests/                      # pruebas de UI (SauceDemo)
│   ├── test_login.py           #   parametrizado con datos/login.csv
│   ├── test_navegacion.py
│   ├── test_carrito.py         #   parametrizado con datos/productos.json
│   └── test_checkout.py        #   compra completa + datos incompletos (checkout_incompleto.json)
├── tests_api/
│   └── test_posts_api.py       # pruebas de API (JSONPlaceholder)
├── features/                   # BDD con Behave
│   ├── login.feature
│   ├── cart.feature
│   ├── environment.py          #   hooks: navegador, limpieza entre escenarios, captura al fallar
│   └── steps/
├── tests_behave/
│   └── test_behave_suite.py    # pytest corre Behave (@smoke y @regression)
├── utils/
│   ├── driver.py               # crea Chrome (con HEADLESS=1 sin ventana)
│   ├── logger.py               # log en logs/suite.log
│   ├── datos.py                # lectura de CSV y JSON
│   └── api_client.py           # pedidos HTTP y validaciones de API
├── datos/                      # datos de prueba (CSV y JSON)
├── reports/                    # se genera al correr: reportes HTML y capturas
├── logs/                       # se genera al correr: suite.log
├── conftest.py                 # fixtures, captura al fallar y personalización del reporte
├── pytest.ini
├── behave.ini
└── requirements.txt
```

## Casos de prueba

**UI – SauceDemo (22 tests)**

| Archivo | Qué prueba | Tipo |
|---|---|---|
| `test_login.py` | Login con 7 combinaciones del CSV: 3 usuarios que entran y 4 que no (bloqueado, clave incorrecta, usuario inexistente, campos vacíos) + smoke | positivo y negativo |
| `test_navegacion.py` | El detalle de un producto muestra el mismo nombre y precio que la lista; ordenar por precio; cerrar sesión y no poder volver por URL | positivo y negativo |
| `test_carrito.py` | Agregar cada producto del JSON (precio y contador); quitar un producto; smoke | positivo |
| `test_checkout.py` | Compra completa: 2 productos, datos de envío, resumen (subtotal + 8 % de impuesto = total) y "Thank you for your order!" | flujo e2e |
| `test_checkout.py` | Formulario sin nombre, sin apellido o sin código postal: muestra el error y no avanza | negativo |

**API – JSONPlaceholder (7 tests)**

| Test | Método | Qué valida |
|---|---|---|
| `test_obtener_post_por_id` | GET `/posts/1` | 200, estructura y tipos (`userId`, `id`, `title`, `body`), id correcto |
| `test_listar_posts_de_un_usuario` | GET `/posts?userId=1` | 200, 10 posts, todos del usuario 1 |
| `test_post_inexistente_devuelve_404` | GET `/posts/99999` | 404 y JSON vacío (escenario de error) |
| `test_crear_post` (×2, datos de `posts_nuevos.json`) | POST `/posts` | 201, estructura y que devuelva lo enviado |
| `test_eliminar_post` | DELETE `/posts/1` | 200 y JSON vacío |
| `test_ciclo_de_vida_post` | POST → PATCH → DELETE | Encadenado: usa el id que devolvió el POST |

En todos se valida además que la respuesta sea JSON y que llegue en menos de 3 segundos.

**BDD – Behave (7 escenarios)**: login exitoso (`@smoke`), 4 logins fallidos con un Esquema del escenario,
agregar la mochila al carrito y agregar varios productos (`@regression`).

Cada test de UI abre su propio navegador y hace su propio login, así que los tests son independientes:
se pueden correr solos o en cualquier orden.

## Instalación

Requisitos: Python 3.12 y Google Chrome (Selenium descarga solo el driver).

```bash
git clone https://github.com/Rgiliberti/proyecto-final-automation-testing-romina-giliberti.git
cd proyecto-final-automation-testing-romina-giliberti
pip install -r requirements.txt
```

## Cómo ejecutar

```bash
pytest                       # todo: UI + API + BDD (unos 2 minutos)
pytest -m smoke              # solo lo básico
pytest -m api                # solo API (no abre el navegador)
pytest tests/test_checkout.py   # un archivo
behave                       # solo los escenarios BDD
behave -t @smoke
```

Para correr sin abrir la ventana del navegador:

```bash
HEADLESS=1 pytest            # Linux / Mac / Git Bash
$env:HEADLESS="1"; pytest    # PowerShell
```

En Windows conviene además `PYTHONUTF8=1` para que los acentos de Behave salgan bien en la consola.

## Cómo leer los reportes

Después de cada corrida:

- **`reports/report.html`**: se abre con el navegador. Arriba está el resumen (cuántos pasaron,
  fallaron o se saltearon) y los metadatos (proyecto, autora, versión de Python). En la tabla
  hay una fila por test con su estado, su duración y la URL donde terminó. Al hacer clic en
  un test que falló se ve el error, el log de ese test y la captura de pantalla.
- **`reports/screens/`**: una captura por cada test de UI que falló, con el nombre del test y la
  fecha y hora (por ejemplo `test_compra_completa_2026-11-08_22-10-35.png`).
- **`reports/behave_smoke.html` / `behave_regression.html`**: reporte de los escenarios BDD, con
  cada paso en verde o rojo. Los `.json` son la misma información para otras herramientas.
- **`logs/suite.log`**: los pasos de cada test con fecha y hora (abrir página, login, productos
  agregados, pedidos a la API) y el resultado. Las fallas quedan como `ERROR` con la ruta de la captura.

## Integración continua

El workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) corre en cada push o pull request a `main`:

1. Instala Python 3.12 y las dependencias.
2. Corre las pruebas **smoke**. Si alguna falla, el pipeline se corta y queda en rojo.
3. Corre el resto de las pruebas.
4. Sube los reportes (`reports/`) y el log (`logs/`) como artefactos, aunque haya fallas. Se guardan 90 días.

Los artefactos se descargan desde la pestaña **Actions** → la corrida → **Artifacts**.
El badge de arriba muestra si la última corrida pasó (verde) o falló (rojo).

## Decisiones

- **JSONPlaceholder en vez de reqres.in**: reqres.in limita la demo gratuita a 40 pedidos por día
  por IP, y en GitHub Actions eso hacía fallar los tests por algo ajeno al proyecto. JSONPlaceholder
  no tiene límite. Como no guarda nada, el POST siempre devuelve `id` 101 y el PATCH/DELETE responden
  aunque el post no exista.
- **Solo esperas explícitas** (`WebDriverWait`), nunca `time.sleep` ni `implicitly_wait`.
- **Behave usa un solo navegador** para todos los escenarios (es más rápido); antes de cada escenario
  se borran las cookies y el `localStorage` para que no queden sesión ni carrito del anterior.
