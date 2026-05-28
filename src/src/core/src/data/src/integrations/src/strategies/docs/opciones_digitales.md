# Opciones Digitales - IQ Option API

## Índice

1. Modo de ataque más cercano
2. Obtener lista de strikes
3. Suscribirse a strikes
4. Comprar digital
5. Comprar al precio actual
6. Beneficio después de la venta
7. Beneficio actual
8. Comprobar resultado de una operación
9. Cerrar operación digital
10. Obtener datos digitales
11. Exposición activa

---

# 1. Modo de ataque más cercano

Ejemplo completo:

```python
from iqoptionapi.stable_api import IQ_Option
import random

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

ACTIVES = "EURUSD"
duration = 1
amount = 1

I_want_money.subscribe_strike_list(ACTIVES, duration)

data = I_want_money.get_realtime_strike_list(ACTIVES, duration)

price_list = list(data.keys())
choose_price = price_list[random.randint(0, len(price_list)-1)]

instrument_id = data[choose_price]["call"]["id"]
profit = data[choose_price]["call"]["profit"]

print("Precio:", choose_price)
print("ID:", instrument_id)
print("Profit:", profit)

buy_check, id = I_want_money.buy_digital(amount, instrument_id)

if buy_check:
    while True:
        check_close, win_money = I_want_money.check_win_digital_v2(id, 5)

        if check_close:
            print("Resultado:", win_money)
            break

I_want_money.unsubscribe_strike_list(ACTIVES, duration)
```

---

# 2. Obtener todos los datos de la lista de strikes

```python
from iqoptionapi.stable_api import IQ_Option
import time

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

ACTIVES = "EURUSD"
duration = 1

I_want_money.subscribe_strike_list(ACTIVES, duration)

while True:
    data = I_want_money.get_realtime_strike_list(ACTIVES, duration)

    for price in data:
        print(price, data[price])

    time.sleep(5)
```

---

# 3. Suscribirse a strikes

```python
I_want_money.subscribe_strike_list(ACTIVES, duration)
```

---

# Obtener lista de strikes en tiempo real

```python
I_want_money.get_realtime_strike_list(ACTIVES, duration)
```

---

# Cancelar suscripción

```python
I_want_money.unsubscribe_strike_list(ACTIVES, duration)
```

---

# 4. Comprar Digital

```python
buy_check, id = I_want_money.buy_digital(amount, instrument_id)
```

---

# 5. Comprar Digital al precio actual

```python
from iqoptionapi.stable_api import IQ_Option

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

ACTIVES = "EURUSD"
duration = 1
amount = 1
action = "call"

print(
    I_want_money.buy_digital_spot(
        ACTIVES,
        amount,
        action,
        duration
    )
)
```

---

# 6. Beneficio después de la venta

```python
from iqoptionapi.stable_api import IQ_Option

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

ACTIVES = "EURUSD"
duration = 1
amount = 100
action = "put"

I_want_money.subscribe_strike_list(ACTIVES, duration)

_, id = I_want_money.buy_digital_spot(
    ACTIVES,
    amount,
    action,
    duration
)

while True:
    pl = I_want_money.get_digital_spot_profit_after_sale(id)

    if pl is not None:
        print(pl)
```

---

# 7. Beneficio actual

```python
from iqoptionapi.stable_api import IQ_Option
import time

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

ACTIVES = "EURUSD"
duration = 1

I_want_money.subscribe_strike_list(ACTIVES, duration)

while True:
    profit = I_want_money.get_digital_current_profit(
        ACTIVES,
        duration
    )

    print(profit)

    time.sleep(1)
```

---

# 8. Comprobar resultado de una operación

## check_win_digital()

```python
I_want_money.check_win_digital(id, polling_time)
```

## check_win_digital_v2()

```python
check_close, win_money = (
    I_want_money.check_win_digital_v2(id)
)
```

### Ejemplo

```python
from iqoptionapi.stable_api import IQ_Option

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

ACTIVES = "EURUSD"

_, id = I_want_money.buy_digital_spot(
    ACTIVES,
    1,
    "call",
    1
)

while True:
    check, win = I_want_money.check_win_digital_v2(id)

    if check:
        break

print("Resultado:", win)
```

---

# 9. Cerrar operación digital

```python
I_want_money.close_digital_option(id)
```

---

# 10. Obtener datos digitales

## Obtener una posición

```python
print(I_want_money.get_digital_position(id))
```

## Obtener posiciones abiertas

```python
print(
    I_want_money.get_positions(
        "digital-option"
    )
)
```

## Historial

```python
print(
    I_want_money.get_position_history(
        "digital-option"
    )
)
```

---

# 11. Exposición activa

```python
from iqoptionapi.stable_api import IQ_Option

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

instrument_type = "digital-option"
active = "EURUSD"
exp = 1

print(
    I_want_money.get_active_exposure(
        instrument_type,
        active,
        exp
    )
)
```

---

## Notas

- `duration` puede ser 1 o 5 minutos.
- `action` puede ser `call` o `put`.
- Es obligatorio llamar a `subscribe_strike_list()` antes de usar `get_realtime_strike_list()`.
- Para operaciones digitales se recomienda usar `check_win_digital()` o `check_win_digital_v2()`.
- Siempre cancelar las suscripciones cuando no se utilicen.