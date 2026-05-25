from iqoptionapi.stable_api import IQ_Option
import time

# ==============================
# ⚙️ CREDENCIALES
# ==============================
EMAIL    = "GMAIL.COM"
PASSWORD = "CONTRASEÑA "

MONTO     = 1
DIRECCION = "PUT"
DURACION  = 1

# ==============================
# 📋 NOMBRES EXACTOS VERIFICADOS EN iqoptionapi
# ==============================
TODOS_OTC = [
    "EURUSD",
    "GBPUSD",
    "EURJPY",
    "EURGBP",
    "USDJPY",
    "USDCHF",
    "USDCAD",
    "NZDUSD",
    "AUDUSD",
    "CADJPY",
    "AUDCAD",
    "GBPJPY",
    "GBPAUD",
    "GBPCAD",
    "GBPCHF",
    "EURCAD",
    "EURCHF",
    "AUDCHF",
    "AUDNZD",
    "NZDCAD",
    "NZDJPY",
    "NZDCHF",
    "CADJPY",
    "CADCHF",
    "CHFJPY",
]

# ==============================
# 🔌 CONEXIÓN
# ==============================
print("🔌 Conectando...")
Iq = IQ_Option(EMAIL, PASSWORD)
Iq.connect()
time.sleep(2)

if not Iq.check_connect():
    print("❌ No se pudo conectar.")
    exit()

print("✅ Conectado correctamente")
Iq.change_balance("PRACTICE")
print(f"💼 Cuenta: PRACTICE")
print(f"🔍 Probando {len(TODOS_OTC)} activos OTC...\n")

# ==============================
# 🔄 FASE 1 — DETECTAR DISPONIBLES
# ==============================
print("=" * 45)
print("FASE 1 — Detectando activos disponibles...")
print("=" * 45)

disponibles = []

for ACTIVO in TODOS_OTC:
    try:
        estado, op_id = Iq.buy(MONTO, ACTIVO, DIRECCION, DURACION)
        if estado:
            disponibles.append((ACTIVO, op_id))
            print(f"  ✅ {ACTIVO}")
        else:
            print(f"  ❌ {ACTIVO} — no disponible")
    except KeyError:
        print(f"  ⚠️ {ACTIVO} — nombre no reconocido por la librería")
    except Exception as e:
        print(f"  ⚠️ {ACTIVO} — error: {e}")
    time.sleep(0.5)

# ==============================
# 📊 FASE 2 — ESPERAR RESULTADOS
# ==============================
print(f"\n{'='*45}")
print(f"FASE 2 — {len(disponibles)} operaciones abiertas, esperando...")
print(f"{'='*45}")

if disponibles:
    print(f"⏳ Esperando {DURACION} min...")
    time.sleep(DURACION * 60 + 5)

resultados = []
for ACTIVO, op_id in disponibles:
    resultado = Iq.check_win_v3(op_id)
    if resultado is None:
        resultados.append((ACTIVO, "⚠️ Sin resultado"))
    elif resultado > 0:
        resultados.append((ACTIVO, f"✅ Ganada +${resultado:.2f}"))
    else:
        resultados.append((ACTIVO, f"❌ Perdida ${resultado:.2f}"))

# ==============================
# 📊 RESUMEN FINAL
# ==============================
print(f"\n{'='*45}")
print("📊 RESUMEN FINAL")
print(f"{'='*45}")
print(f"Probados:      {len(TODOS_OTC)}")
print(f"Disponibles:   {len(disponibles)}")
print(f"{'='*45}")

if resultados:
    print("\nResultados:")
    for activo, res in resultados:
        print(f"  {activo:25s} → {res}")

print(f"\n{'='*45}")
print("✅ Copia esta lista en tu bot:")
print("ACTIVOS = [")
for activo, _ in disponibles:
    print(f'    "{activo}",')
print("]")
print(f"{'='*45}")
