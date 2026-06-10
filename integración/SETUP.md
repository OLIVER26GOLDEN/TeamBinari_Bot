# ⚙️ Configuración del Bot — TeamBinari Bot

## 📦 Dependencias

Instala las dependencias con:

```bash
pip install iqoption
```

```
iqoptionapi
python-telegram-bot==13.15
requests
```

---

## 🤖 Paso 1 — Crear tu bot en Telegram con BotFather

> BotFather es el bot oficial de Telegram para crear y gestionar bots.

### ¿Cómo encontrarlo?

1. Abre Telegram (móvil o escritorio)
2. En el **buscador** escribe: `BotFather`
3. Selecciona el que tiene el **tick azul verificado** ✅
4. Pulsa **START** o escribe `/start`

---

### Comandos que usarás:

| Comando | Qué hace |
|---|---|
| `/newbot` | Crear un bot nuevo |
| `/mybots` | Ver tus bots existentes |
| `/token` | Obtener o regenerar el token |

---

### Proceso paso a paso:

```
Tú      →  /newbot
BotFather → "¿Cómo se va a llamar tu bot?"

Tú      →  TeamBinari Bot          ← nombre visible (puede ser cualquiera)
BotFather → "Elige un username, debe terminar en 'bot'"

Tú      →  oliver26bot             ← username único (termina en bot)
BotFather → "¡Listo! Tu token es:"
            7084965418:AAEmWgPVE9_wB2R9sVvV4XOQryDpB79uBYk
```

> ⚠️ **Guarda ese token.** Es la clave de acceso de tu bot.  
> **Nunca lo subas a GitHub.**

---

## 🔐 Paso 2 — Obtener tu Chat ID

Para que el bot sepa a quién enviarle las alertas, necesitas tu `CHAT_ID`:

1. Busca en Telegram: `@userinfobot`
2. Pulsa START
3. Te responde con tu ID numérico, algo como: `123456789`

---

## 🛠️ Paso 3 — Configurar credenciales

Crea el archivo `config.py` en la raíz del proyecto:

```python
# ─── IQ Option ───────────────────────────
IQ_EMAIL    = "tu_email@gmail.com"
IQ_PASSWORD = "tu_contraseña"

# ─── Telegram ────────────────────────────
BOT_TOKEN = "7084965418:AAEmWgPVE9_..."   # token de BotFather
CHAT_ID   = "123456789"                    # tu ID de @userinfobot
```

Añade esto a tu `.gitignore`:

```
config.py
```

---

## ▶️ Paso 4 — Ejecutar el bot

```bash
python bot.py
```

Si todo está bien verás en consola:

```
[✔] Conectado a IQ Option
[✔] Telegram OK
[→] Monitoreando: EURUSD, GBPUSD, AUDUSD...
```

Y recibirás las señales directamente en Telegram. 📲
