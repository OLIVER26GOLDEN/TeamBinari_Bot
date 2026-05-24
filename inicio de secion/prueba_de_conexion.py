from iqoptionapi.stable_api import IQ_Option
import time
import requests

# ==============================
# 🔐 CREDENCIALES
# ==============================
EMAIL    = "GMAIL.COM"
PASSWORD = "CONTRASEÑA "

# ==============================
# 📩 TELEGRAM
# ==============================
TELEGRAM_TOKEN = "TOKEN_TELEGRAM"
CHAT_ID        = "CHAT_ID"

ACTIVO = "AUDCAD-OTC"

# ==============================
# 📬 TEST TELEGRAM
# ==============================
def test_telegram():
    print("\n📬 Probando Telegram...")
    try:
        url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": "✅ TEST: Telegram funcionando correctamente"}
        r    = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print("   ✅ Telegram OK")
            return True
        else:
            print(f"   ❌ Telegram falló — Status: {r.status_code} | {r.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error Telegram: {e}")
        return False

# ==============================
# 🔌 TEST IQ OPTION
# ==============================
def test_iqoption():
    print("\n🔌 Probando conexión IQ Option...")
    try:
        Iq = IQ_Option(EMAIL, PASSWORD)
        Iq.connect()
        time.sleep(2)

        if not Iq.check_connect():
            print("   ❌ No se pudo conectar a IQ Option")
            return None

        print("   ✅ Conexión IQ Option OK")

        # --- Balance REAL ---
        Iq.change_balance("REAL")
        balance_real = Iq.get_balance()
        print(f"   💰 Balance REAL:  ${balance_real:.2f}")

        # --- Balance PRÁCTICA ---
        Iq.change_balance("PRACTICE")
        balance_prac = Iq.get_balance()
        print(f"   🎮 Balance PRÁCTICA: ${balance_prac:.2f}")

        # --- Verificar activo disponible ---
        print(f"\n📊 Verificando activo {ACTIVO}...")
        Iq.change_balance("REAL")
        activos = Iq.get_all_open_time()

        # Buscar en binarias y digitales
        disponible_bin = activos.get("turbo", {}).get(ACTIVO, {}).get("open", False)
        disponible_dig = activos.get("digital", {}).get(ACTIVO, {}).get("open", False)

        if disponible_bin:
            print(f"   ✅ {ACTIVO} disponible en Binarias")
        else:
            print(f"   ⚠️  {ACTIVO} NO disponible en Binarias (puede ser horario)")

        if disponible_dig:
            print(f"   ✅ {ACTIVO} disponible en Digitales")
        else:
            print(f"   ⚠️  {ACTIVO} NO disponible en Digitales (puede ser horario)")

        # --- Obtener velas de prueba ---
        print(f"\n📈 Obteniendo velas de prueba de {ACTIVO}...")
        velas = Iq.get_candles(ACTIVO, 60, 5, time.time())

        if velas and len(velas) > 0:
            print(f"   ✅ Velas recibidas: {len(velas)}")
            ultima = velas[-1]
            print(f"   🕯  Última vela → Open: {ultima['open']} | Close: {ultima['close']} | Min: {ultima['min']} | Max: {ultima['max']}")
        else:
            print("   ⚠️  No se pudieron obtener velas")

        return Iq

    except Exception as e:
        print(f"   ❌ Error IQ Option: {e}")
        return None

# ==============================
# 🚀 EJECUTAR TESTS
# ==============================
print("=" * 50)
print("🤖 TEST DE CONEXIÓN — BOT AUDCAD")
print("=" * 50)

ok_telegram  = test_telegram()
iq           = test_iqoption()
ok_iqoption  = iq is not None

# --- Resumen final ---
print("\n" + "=" * 50)
print("📋 RESUMEN")
print("=" * 50)
print(f"  Telegram  : {'✅ OK' if ok_telegram else '❌ FALLO'}")
print(f"  IQ Option : {'✅ OK' if ok_iqoption else '❌ FALLO'}")

if ok_telegram and ok_iqoption:
    print("\n🟢 Todo listo — El bot puede operar correctamente")
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": "🟢 TEST COMPLETO: Bot listo para operar ✅"}
    )
else:
    print("\n🔴 Hay problemas — Revisa los errores arriba antes de arrancar el bot")

print("=" * 50)