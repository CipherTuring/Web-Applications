# Guía de capturas para el reporte

Cada paso indica qué correr y qué fotografiar. **El orden importa**: la
secuencia reproduce exactamente los números que ya están escritos en el
reporte (ids, stocks, cantidades). Si te salteás un paso, los números de las
capturas no van a coincidir con el texto.

Guardá cada captura en `report/img/` con el nombre indicado. No hay que tocar
el `.tex`: al recompilar, la caja gris se reemplaza sola por tu imagen.

---

## Preparación

### Usá Git Bash, no PowerShell

En PowerShell, `curl` es un alias de `Invoke-WebRequest` y **no acepta** la
sintaxis `-X POST -d '{...}'` de estos comandos. Todos los comandos de esta
guía son para **Git Bash**.

### Tres terminales

Abrí tres ventanas de Git Bash, todas posicionadas en la carpeta del proyecto:

```bash
cd "/c/Users/ismae/Desktop/Personal/vscode/Web-Applications/fastapi-orm-workshop"
```

| Terminal | Para qué |
|---|---|
| **A** | Uvicorn corriendo (de acá salen las capturas del SQL generado) |
| **B** | Comandos `curl` y el cliente Python |
| **C** | Consola de MySQL |

### En la terminal C, poné `mysql` en el PATH

Así los comandos quedan cortos y las capturas se ven limpias:

```bash
export PATH="$PATH:/c/Program Files/MySQL/MySQL Server 8.0/bin"
```

### Paso 0 — Reiniciar los datos

La base tiene datos de pruebas anteriores. Este script borra todo y reinicia
los contadores de `id`, para que los ids empiecen en 1 como dice el reporte:

```bash
mysql -u ormuser -p orm_workshop < server/reset_data.sql
```

Contraseña: `ormpass123`

### Paso 0.1 — Levantar la API (terminal A)

```bash
./.venv/Scripts/python.exe -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

Dejala corriendo hasta el final. Agrandá esta ventana: de acá salen dos
capturas y el SQL es ancho.

---

## FIGURA 1 — `fig01-show-tables`

**Terminal C:**

```bash
mysql -u ormuser -p orm_workshop
```

```sql
SHOW TABLES;
```

📸 **Foto:** la ventana mostrando el comando y las cuatro tablas
(`customers`, `order_items`, `orders`, `products`).

Dejá abierta la sesión de MySQL, la vas a seguir usando.

---

## FIGURA 2 — `fig02-crud-curl`

**Terminal B**, los cinco comandos de Customer en orden:

```bash
curl -X POST http://127.0.0.1:8000/customers -H "Content-Type: application/json" -d '{"name":"Alice Brown","email":"alice@example.com"}'

curl -X POST http://127.0.0.1:8000/customers -H "Content-Type: application/json" -d '{"name":"John Smith","email":"john@example.com"}'

curl -X POST http://127.0.0.1:8000/customers -H "Content-Type: application/json" -d '{"name":"Maria Lopez","email":"maria@example.com"}'

curl -X PUT http://127.0.0.1:8000/customers/2 -H "Content-Type: application/json" -d '{"name":"John Anderson"}'

curl -X DELETE http://127.0.0.1:8000/customers/3
```

📸 **Foto:** que se vea al menos el `POST` que crea a Alice con su respuesta
JSON (con el `id` generado) y el `PUT` que renombra a John con su respuesta.

---

## Paso intermedio — Crear los productos

**Terminal B** (sin foto):

```bash
curl -X POST http://127.0.0.1:8000/products -H "Content-Type: application/json" -d '{"name":"Mechanical Keyboard","price":85.50,"stock":20}'

curl -X POST http://127.0.0.1:8000/products -H "Content-Type: application/json" -d '{"name":"Wireless Mouse","price":28.50,"stock":40}'

curl -X POST http://127.0.0.1:8000/products -H "Content-Type: application/json" -d '{"name":"USB-C Hub","price":42.00,"stock":15}'

curl -X POST http://127.0.0.1:8000/products -H "Content-Type: application/json" -d '{"name":"Webcam","price":65.00,"stock":10}'

curl -X PUT http://127.0.0.1:8000/products/3 -H "Content-Type: application/json" -d '{"stock":25}'
```

---

## FIGURA 3 — `fig03-crud-mysql`

**Terminal C:**

```sql
SELECT * FROM customers;
SELECT * FROM products;
```

📸 **Foto:** los clientes 1 y 2 (John ya renombrado a "John Anderson", Maria
ausente porque fue borrada) y los cuatro productos con el USB-C Hub en
**stock 25**.

---

## FIGURA 4 — `fig04-nested-insert-mysql`

**Terminal B** — crear la orden anidada:

```bash
curl -X POST http://127.0.0.1:8000/orders -H "Content-Type: application/json" -d '{"customer_id":1,"items":[{"product_id":1,"quantity":2},{"product_id":2,"quantity":1},{"product_id":3,"quantity":3}]}'
```

**Terminal C:**

```sql
SELECT * FROM orders;
SELECT * FROM order_items;
```

📸 **Foto:** una fila en `orders` (id 1, `customer_id` 1) y **tres** filas en
`order_items`, todas con `order_id` = 1 y `product_id` 1, 2 y 3.

> Estas son las claves foráneas que el programa nunca asignó a mano.

---

## FIGURA 5 — `fig05-update-sql`

**Terminal B:**

```bash
curl -X PUT http://127.0.0.1:8000/orders/1/status -H "Content-Type: application/json" -d '{"status":"processing"}'
```

📸 **Foto — de la TERMINAL A (Uvicorn)**, inmediatamente después. Buscá y
encuadrá estas tres líneas:

```
UPDATE orders SET status=%(status)s WHERE orders.id = %(orders_id)s
[generated in 0.00099s] {'status': 'processing', 'orders_id': 1}
COMMIT
```

> Es la evidencia central de la sección 7: una sola asignación de atributo en
> Python produjo ese `UPDATE` con una sola columna en el `SET`.

---

## FIGURA 6 — `fig06-cascade-before`

**Terminal C:**

```sql
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT id, name, stock FROM products;
```

📸 **Foto:** la orden 1, sus tres items y los cuatro productos.

---

## FIGURA 7 — `fig07-cascade-after`

**Terminal B:**

```bash
curl -X DELETE http://127.0.0.1:8000/orders/1
```

**Terminal C** — exactamente las mismas tres consultas de la figura 6:

```sql
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT id, name, stock FROM products;
```

📸 **Foto:** `orders` y `order_items` vacías (`Empty set`) y los cuatro
productos intactos.

> El contraste entre la figura 6 y la 7 es toda la evidencia de la cascada.
> Tratá de que las dos capturas tengan el mismo encuadre.

---

## FIGURA 8 — `fig08-transaction-stock`

**Terminal B**, los tres comandos seguidos y en una sola captura:

```bash
curl -s http://127.0.0.1:8000/products | python -m json.tool

curl -X POST http://127.0.0.1:8000/orders -H "Content-Type: application/json" -d '{"customer_id":2,"items":[{"product_id":1,"quantity":2},{"product_id":2,"quantity":3}]}'

curl -s http://127.0.0.1:8000/products | python -m json.tool
```

📸 **Foto:** el inventario antes, el POST, y el inventario después. Tiene que
verse que el producto 1 bajó de **18 a 16** y el producto 2 de **39 a 36**.

> Si no entra todo, achicá la letra de la terminal (Ctrl + rueda del mouse).

---

## FIGURA 9 — `fig09-rollback`

**Terminal B**, los tres comandos seguidos:

```bash
curl -s http://127.0.0.1:8000/products | python -m json.tool

curl -w "\nHTTP %{http_code}\n" -X POST http://127.0.0.1:8000/orders -H "Content-Type: application/json" -d '{"customer_id":1,"items":[{"product_id":1,"quantity":1},{"product_id":4,"quantity":1000}]}'

curl -s http://127.0.0.1:8000/products | python -m json.tool
```

📸 **Foto:** el inventario antes, el error
`{"detail":"Insufficient stock for Webcam"}` con el `HTTP 400`, y el
inventario después.

> **Lo esencial que tiene que leerse:** el stock del producto 1 es **16 en los
> dos listados**. No bajó a 15, aunque el programa ya le había restado 1 antes
> de detectar la falla del producto 4. Esta es la captura más importante del
> reporte.

---

## FIGURA 10 — `fig10-client-menu`

**Terminal B** (desde la raíz del proyecto, si no, no encuentra el JSON):

```bash
./.venv/Scripts/python.exe client/client.py
```

Cuando aparezca el menú:

- Escribí `5` (Create order from JSON) y Enter
- Cuando pida el nombre del archivo, Enter (usa el default)

📸 **Foto:** el menú completo con sus opciones y la ejecución exitosa: la
línea `HTTP: 200` y el JSON de la orden creada.

Después escribí `0` para salir.

---

## FIGURA 11 — `fig11-final-exercise`

**Terminal B:**

```bash
curl -s http://127.0.0.1:8000/products/1/customers | python -m json.tool

curl -s http://127.0.0.1:8000/products/4/customers | python -m json.tool
```

📸 **Foto:** el primero devolviendo los dos clientes (Alice Brown y John
Anderson) y, si entra, el segundo devolviendo `[]`.

> El `[]` del producto 4 es interesante: la Webcam nunca se vendió, porque la
> única orden que la pidió fue justamente la que se revirtió.

---

## Checklist

| # | Archivo | Terminal | Listo |
|---|---|---|---|
| 1 | `fig01-show-tables` | C (MySQL) | [ ] |
| 2 | `fig02-crud-curl` | B (curl) | [ ] |
| 3 | `fig03-crud-mysql` | C (MySQL) | [ ] |
| 4 | `fig04-nested-insert-mysql` | C (MySQL) | [ ] |
| 5 | `fig05-update-sql` | **A (Uvicorn)** | [ ] |
| 6 | `fig06-cascade-before` | C (MySQL) | [ ] |
| 7 | `fig07-cascade-after` | C (MySQL) | [ ] |
| 8 | `fig08-transaction-stock` | B (curl) | [ ] |
| 9 | `fig09-rollback` | B (curl) | [ ] |
| 10 | `fig10-client-menu` | B (cliente) | [ ] |
| 11 | `fig11-final-exercise` | B (curl) | [ ] |

Guardalas en `report/img/` con esos nombres exactos y extensión `.png`, `.jpg`,
`.jpeg` o `.pdf`.

---

## Si algo sale mal

**Un `curl` devuelve error 500 al crear un cliente:** el email ya existe
(la columna es `unique`). Corré el Paso 0 de nuevo y empezá desde la figura 1.

**Los números no coinciden con el reporte:** hiciste alguna petición de más.
Corré el Paso 0 y repetí la secuencia completa desde la figura 1.

**`Address already in use` al levantar Uvicorn:** ya hay un servidor en el
puerto 8000. Cerralo con Ctrl+C en la terminal donde esté corriendo.

**El cliente no encuentra `client/data/order.json`:** lo lanzaste desde otra
carpeta. Tiene que ser desde `fastapi-orm-workshop/`.
