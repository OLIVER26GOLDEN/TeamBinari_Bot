# 📈 Opciones Binarias con IQ Option API

## Introducción

Este documento recopila ejemplos y notas sobre el uso de opciones binarias mediante la librería `iqoptionapi`.

---

## Comprar una operación

### Ejemplo básico

```python
from iqoptionapi.stable_api import IQ_Option
import time

iq = IQ_Option("email", "password")
iq.connect()

amount = 1
asset = "EURUSD"
action = "call"
expiration = 1

check, order_id = iq.buy(amount, asset, action, expiration)

if check:
    print("Operación abierta correctamente")
else:
    print("Error al abrir la operación")
```

### Parámetros

| Parámetro | Descripción |
|------------|------------|
| amount | Cantidad a invertir |
| asset | Activo (EURUSD, EURGBP, etc.) |
| action | `call` o `put` |
| expiration | Tiempo de expiración en minutos |

---

## Comprar múltiples operaciones

```python
from iqoptionapi.stable_api import IQ_Option

iq = IQ_Option("email", "password")
iq.connect()

amounts = [1, 1]
assets = ["EURUSD", "EURAUD"]
actions = ["call", "call"]
expirations = [1, 1]

ids = iq.buy_multi(
    amounts,
    assets,
    actions,
    expirations
)

print(ids)
```

---

## Comprobar resultado de una operación

### check_win()

```python
resultado = iq.check_win(order_id)
print(resultado)
```

### check_win_v2()

```python
resultado = iq.check_win_v2(order_id, 3)
print(resultado)
```

### check_win_v3()

```python
resultado = iq.check_win_v3(order_id)
print(resultado)
```

---

## Venta anticipada

```python
iq.sell_option(order_id)
```

O varias operaciones:

```python
iq.sell_option([id1, id2, id3])
```

---

## Tiempo restante para comprar

```python
remaining = iq.get_remaning(1)

if remaining < 4:
    print("Momento de entrada")
```

---

## Estado de ánimo de los traders

```python
asset = "EURUSD"

iq.start_mood_stream(asset)

print(
    iq.get_traders_mood(asset)
)

iq.stop_mood_stream(asset)
```

---

## Información histórica

```python
print(
    iq.get_optioninfo(10)
)
```

```python
print(
    iq.get_optioninfo_v2(10)
)
```

---

## Exposición activa

```python
print(
    iq.get_active_exposure(
        "turbo-option",
        "EURUSD",
        1
    )
)
```

---

## Notas

- Utilizar siempre cuenta demo para pruebas.
- No almacenar contraseñas en el código fuente.
- No subir credenciales a GitHub.
- Verificar siempre que el activo esté abierto antes de operar.