# Velas

## Obtener Velas

Obtiene velas históricas. No es un flujo en tiempo real.

### Sintaxis

```python
I_want_money.get_candles(ACTIVES, interval, count, endtime)

# ACTIVES: Ejemplo "EURUSD" o "EURGBP"
# interval: Duración de cada vela
# count: Cantidad de velas a obtener
# endtime: Tiempo final para buscar velas históricas
```

### Ejemplo

```python
from iqoptionapi.stable_api import IQ_Option
import time

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

end_from_time = time.time()
ANS = []

for i in range(70):
    data = I_want_money.get_candles("EURUSD", 60, 1000, end_from_time)
    ANS = data + ANS
    end_from_time = int(data[0]["from"]) - 1

print(ANS)
```

---

# Velas en Tiempo Real

## Indicadores con TA-Lib

### Ejemplo EMA

```python
from talib.abstract import *
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np

print("login...")

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

goal = "EURUSD"
size = 10
timeperiod = 10
maxdict = 20

print("start stream...")
I_want_money.start_candles_stream(goal, size, maxdict)

print("Start EMA Sample")

while True:
    candles = I_want_money.get_realtime_candles(goal, size)

    inputs = {
        'open': np.array([]),
        'high': np.array([]),
        'low': np.array([]),
        'close': np.array([]),
        'volume': np.array([])
    }

    for timestamp in candles:
        inputs["open"] = np.append(inputs["open"], candles[timestamp]["open"])
        inputs["high"] = np.append(inputs["high"], candles[timestamp]["max"])
        inputs["low"] = np.append(inputs["low"], candles[timestamp]["min"])
        inputs["close"] = np.append(inputs["close"], candles[timestamp]["close"])
        inputs["volume"] = np.append(inputs["volume"], candles[timestamp]["volume"])

    print("Show EMA")
    print(EMA(inputs, timeperiod=timeperiod))
    print("\n")

    time.sleep(1)

I_want_money.stop_candles_stream(goal, size)
```

---

## Flujo Básico de Velas en Tiempo Real

### Ejemplo

```python
from iqoptionapi.stable_api import IQ_Option
import time

print("login...")

I_want_money = IQ_Option("email", "password")
I_want_money.connect()

goal = "EURUSD"

size = "all"
# Valores permitidos:
# [1,5,10,15,30,60,120,300,600,900,1800,
# 3600,7200,14400,28800,43200,86400,
# 604800,2592000,"all"]

maxdict = 10

print("start stream...")
I_want_money.start_candles_stream(goal, size, maxdict)

print("Do something...")
time.sleep(10)

print("print candles")

cc = I_want_money.get_realtime_candles(goal, size)

for k in cc:
    print(goal, "size", k, cc[k])

print("stop candle")

I_want_money.stop_candles_stream(goal, size)
```

---

# Tamaños de Velas

| Valor | Duración |
|---------|---------|
| 1 | 1 segundo |
| 5 | 5 segundos |
| 10 | 10 segundos |
| 15 | 15 segundos |
| 30 | 30 segundos |
| 60 | 1 minuto |
| 120 | 2 minutos |
| 300 | 5 minutos |
| 600 | 10 minutos |
| 900 | 15 minutos |
| 1800 | 30 minutos |
| 3600 | 1 hora |
| 7200 | 2 horas |
| 14400 | 4 horas |
| 28800 | 8 horas |
| 43200 | 12 horas |
| 86400 | 1 día |
| 604800 | 1 semana |
| 2592000 | 1 mes |
| all | Todas |

---

# Funciones Disponibles

## Iniciar Canal de Velas

```python
goal = "EURUSD"
size = "all"
maxdict = 10

I_want_money.start_candles_stream(goal, size, maxdict)
```

---

## Obtener Velas en Tiempo Real

> Debe llamarse después de iniciar el stream.

```python
I_want_money.get_realtime_candles(goal, size)
```

---

## Detener Canal de Velas

> Si ya no utilizas las velas en tiempo real, detén la transmisión.

```python
I_want_money.stop_candles_stream(goal, size)
```