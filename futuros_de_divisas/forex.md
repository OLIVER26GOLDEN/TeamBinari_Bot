# Forex, Acciones, Materias Primas, Criptomonedas y ETFs

## Instrument Type e Instrument ID

Puedes buscar `instrument_type` e `instrument_id` en los archivos de activos disponibles.

### Ejemplo de compra

```python
from iqoptionapi.stable_api import IQ_Option

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

instrument_type = "crypto"
instrument_id = "BTCUSD"

side = "buy"  # buy / sell
amount = 1.23

# Multiplicador
leverage = 3

# market / limit / stop
type = "market"

# Solo para órdenes limit
limit_price = None

# Solo para órdenes stop
stop_price = None

# Gestión de riesgo
stop_lose_kind = "percent"
stop_lose_value = 95

take_profit_kind = None
take_profit_value = None

use_trail_stop = True
auto_margin_call = False
use_token_for_commission = False

check, order_id = I_want_money.buy_order(
    instrument_type=instrument_type,
    instrument_id=instrument_id,
    side=side,
    amount=amount,
    leverage=leverage,
    type=type,
    limit_price=limit_price,
    stop_price=stop_price,
    stop_lose_value=stop_lose_value,
    stop_lose_kind=stop_lose_kind,
    take_profit_value=take_profit_value,
    take_profit_kind=take_profit_kind,
    use_trail_stop=use_trail_stop,
    auto_margin_call=auto_margin_call,
    use_token_for_commission=use_token_for_commission
)

print(I_want_money.get_order(order_id))
print(I_want_money.get_positions("crypto"))
print(I_want_money.get_position_history("crypto"))
print(I_want_money.get_available_leverages("crypto", "BTCUSD"))
print(I_want_money.close_position(order_id))
print(I_want_money.get_overnight_fee("crypto", "BTCUSD"))
```

---

# buy_order()

Crea una orden de compra o venta.

## Retorno

```python
(True, order_id)
```

o

```python
(False, False)
```

## Parámetros

| Parámetro | Descripción |
|------------|------------|
| instrument_type | Tipo de instrumento |
| instrument_id | Activo |
| side | buy / sell |
| amount | Cantidad |
| leverage | Apalancamiento |
| type | market / limit / stop |
| limit_price | Solo para órdenes limit |
| stop_price | Solo para órdenes stop |
| stop_lose_kind | price / diff / percent |
| stop_lose_value | Valor stop loss |
| take_profit_kind | price / diff / percent |
| take_profit_value | Valor take profit |
| use_trail_stop | True / False |
| auto_margin_call | True / False |
| use_token_for_commission | True / False |

### Ejemplo

```python
check, order_id = I_want_money.buy_order(
    instrument_type=instrument_type,
    instrument_id=instrument_id,
    side=side,
    amount=amount,
    leverage=leverage,
    type=type,
    limit_price=limit_price,
    stop_price=stop_price,
    stop_lose_kind=stop_lose_kind,
    stop_lose_value=stop_lose_value,
    take_profit_kind=take_profit_kind,
    take_profit_value=take_profit_value,
    use_trail_stop=use_trail_stop,
    auto_margin_call=auto_margin_call,
    use_token_for_commission=use_token_for_commission
)
```

---

# change_order()

Permite modificar una orden existente.

### Ejemplo

```python
ID_Name = "order_id"

stop_lose_kind = None
stop_lose_value = None

take_profit_kind = "percent"
take_profit_value = 200

use_trail_stop = False
auto_margin_call = True

I_want_money.change_order(
    ID_Name=ID_Name,
    order_id=order_id,
    stop_lose_kind=stop_lose_kind,
    stop_lose_value=stop_lose_value,
    take_profit_kind=take_profit_kind,
    take_profit_value=take_profit_value,
    use_trail_stop=use_trail_stop,
    auto_margin_call=auto_margin_call
)
```

---

# get_order()

Obtiene información de una orden.

```python
I_want_money.get_order(order_id)
```

---

# get_pending()

Obtiene órdenes pendientes.

```python
I_want_money.get_pending(instrument_type)
```

---

# get_positions()

Obtiene posiciones abiertas.

### Tipos soportados

- crypto
- forex
- fx-option
- multi-option
- cfd
- digital-option

```python
I_want_money.get_positions(instrument_type)
```

---

# get_position()

Obtiene una posición específica.

```python
I_want_money.get_position(order_id)
```

---

# get_position_history()

Obtiene historial de posiciones.

```python
I_want_money.get_position_history(instrument_type)
```

---

# get_position_history_v2()

Obtiene historial avanzado filtrando fechas.

### Tipos soportados

- crypto
- forex
- fx-option
- turbo-option
- multi-option
- cfd
- digital-option

### Ejemplo

```python
import time
import datetime

instrument_type = ["digital-option"]

limit = 2
offset = 0
start = 0
end = 0

data = I_want_money.get_position_history_v2(
    P_ID,
    start,
    end,
    offset,
    limit,
    instrument_type
)

print(data)
```

### Historial entre fechas

```python
start = int(
    time.mktime(
        datetime.datetime.strptime(
            "2019/1/1",
            "%Y/%m/%d"
        ).timetuple()
    )
)

end = int(
    time.mktime(
        datetime.datetime.strptime(
            "2019/7/1",
            "%Y/%m/%d"
        ).timetuple()
    )
)

data = I_want_money.get_position_history_v2(
    instrument_type,
    limit,
    offset,
    start,
    end
)

print(data)
```

---

# get_available_leverages()

Obtiene los apalancamientos disponibles.

```python
I_want_money.get_available_leverages(
    instrument_type,
    actives
)
```

---

# cancel_order()

Cancela una orden pendiente.

```python
I_want_money.cancel_order(order_id)
```

Retorno:

```python
True
```

o

```python
False
```

---

# close_position()

Cierra una posición abierta.

```python
I_want_money.close_position(order_id)
```

Retorno:

```python
True
```

o

```python
False
```

---

# get_overnight_fee()

Obtiene la comisión nocturna.

```python
I_want_money.get_overnight_fee(
    instrument_type,
    active
)
```

### Ejemplo

```python
print(
    I_want_money.get_overnight_fee(
        "crypto",
        "BTCUSD"
    )
)
```