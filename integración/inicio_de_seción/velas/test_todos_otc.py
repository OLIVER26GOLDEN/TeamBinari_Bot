from iqoptionapi.stable_api import IQ_Option
import time

# ==============================
# ⚙️ CREDENCIALES
# ==============================
EMAIL = "antoni28018@gmail.com"
PASSWORD = "oliver26@A26"


MONTO     = 1
DIRECCION = "PUT"
DURACION  = 1

# ==============================
# 📋 TODOS LOS OTC CONOCIDOS EN IQ OPTION
# ==============================
TODOS_OTC = [
    
    "EURUSD-OTC",
    "GBPUSD-OTC",
    "EURJPY-OTC",
    "EURGBP-OTC",
    "USDCHF-OTC",
    "AUDCAD-OTC",
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
# 🔄 FASE 1 — DETECTAR CUÁLES ESTÁN DISPONIBLES (sin operar)
# ==============================
print("=" * 45)
print("FASE 1 — Detectando activos disponibles...")
print("=" * 45)

disponibles = []

for ACTIVO in TODOS_OTC:
    estado, op_id = Iq.buy(MONTO, ACTIVO, DIRECCION, DURACION)
    if estado:
        disponibles.append((ACTIVO, op_id))
        print(f"  ✅ {ACTIVO} — DISPONIBLE (ID: {op_id})")
    else:
        print(f"  ❌ {ACTIVO} — no disponible")
    time.sleep(0.5)

# ==============================
# 📊 FASE 2 — ESPERAR RESULTADOS DE LOS DISPONIBLES
# ==============================
print(f"\n{'='*45}")
print(f"FASE 2 — Esperando resultados ({len(disponibles)} operaciones abiertas)...")
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
print(f"Total probados:    {len(TODOS_OTC)}")
print(f"Disponibles:       {len(disponibles)}")
print(f"No disponibles:    {len(TODOS_OTC) - len(disponibles)}")
print(f"{'='*45}")

if resultados:
    print("\nResultados:")
    for activo, res in resultados:
        print(f"  {activo:22s} → {res}")

print(f"\n{'='*45}")
print("✅ Activos OTC confirmados para tu bot:")
for activo, _ in disponibles:
    print(f'  "{activo}",')
print(f"{'='*45}")
