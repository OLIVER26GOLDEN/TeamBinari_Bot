from iqoptionapi.stable_api import IQ_Option
import time

# ================= CREDENCIALES =================
EMAIL    = "@gmail.com"
PASSWORD = "contraseña"

# ================= CONFIG =================
ACTIVO = "EURUSD-OTC"   # o EURUSD-OTC
MONTO = 1
EXPIRACION = 1  # minutos

# ================= CONEXION =================
iq = IQ_Option(EMAIL, PASSWORD)
iq.connect()

if iq.check_connect():
    print("✅ Conectado correctamente")
    
    # 👇 CAMBIO CLAVE
    iq.change_balance("PRACTICE")
    print("💰 Cuenta REAL activada")
else:
    print("❌ Error conexión")
    quit()

# ================= ESPERAR NUEVA VELA =================
print("⏳ Esperando nuevo minuto...")

while True:
    if int(time.strftime("%S")) == 59:
        time.sleep(1.2)
        break
    time.sleep(0.1)

# ================= ABRIR OPERACION =================
print("🚀 Enviando operación CALL en REAL...")

status, trade_id = iq.buy(MONTO, ACTIVO, "call", EXPIRACION)

# ================= VALIDACION =================
if not status:
    print("❌ No se pudo abrir la operación")
    quit()

print("✅ Operación abierta")
print("ID:", trade_id)

# ================= RESULTADO =================
print("⏳ Esperando resultado...")

result = iq.check_win_v3(trade_id)

if isinstance(result, tuple):
    # some forks still return (status, value)
    status, win = result
else:
    win = result

if win > 0:
    print(f"✅ Ganada: +{win}")
elif win < 0:
    print(f"❌ Perdida: {win}")
else:
    print("➖ Empate/Doji")










#while True:
   # check, win = iq.check_win_v3(trade_id)

   # if check:
    #    if win > 0:
     #       print("🏆 GANASTE:", win)
    #  elif win == 0:
      #      print("🤝 EMPATE")
       # else:
        #    print("❌ PERDISTE:", win)
        #break

    #time.sleep(1)
