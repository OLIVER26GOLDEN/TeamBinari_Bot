from iqoptionapi.stable_api import IQ_Option
import time
import pandas as pd
import requests

# ==============================
# 🔐 CREDENCIALES
# ==============================
EMAIL = "@gmail.com"
PASSWORD = "PASSWORD"

# ==============================
# ⚙️ CONFIGURACIÓN
# ==============================
ACTIVO = "AUDCAD-OTC"

MAX_OPERACIONES_DIA = 1
operaciones_hoy = 0
dia_actual = time.strftime("%Y-%m-%d")

ultimo_soporte = None
tolerancia = 0.00002

# 🔥 MARTINGALA PERSONALIZADA
secuencia_martingala = [1]
indice_mg = 0

# ==============================
# 📩 TELEGRAM
# ==============================
TELEGRAM_TOKEN = "TOKEN"
CHAT_ID = "ID"

def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": mensaje}
        requests.post(url, data=data)
    except Exception as e:
        print("Error Telegram:", e)

# ==============================
# 🔌 CONEXIÓN
# ==============================
Iq = IQ_Option(EMAIL, PASSWORD)
Iq.connect()

if Iq.check_connect():
    print("✅ Conectado")
    enviar_telegram("🤖 BOT CONECTADO")
else:
    print("❌ Error conexión")
    enviar_telegram("❌ ERROR AL CONECTAR BOT")
    exit()

Iq.change_balance("REAL")
print("🤖 BOT PATRÓN INICIADO - Operaciones 30 segundos")

# ==============================
# 🔍 PATRÓN (4 velas históricas)
# ==============================
def es_patron_4velas(df):
    """
    Evalúa el patrón con las 4 velas históricas cerradas.
    La quinta vela (actual/en curso) se evalúa por separado en el loop.

    Patrón:
      Vela 1: Roja (bajista)
      Vela 2: Verde (alcista)
      Vela 3: Verde (alcista)
      Vela 4: Roja (bajista) — pero sin romper el mínimo de la vela 1
    """
    primera_roja  = df.iloc[0]['close'] < df.iloc[0]['open']
    segunda_verde = df.iloc[1]['close'] > df.iloc[1]['open']
    tercera_verde = df.iloc[2]['close'] > df.iloc[2]['open']
    cuarta_roja   = df.iloc[3]['close'] < df.iloc[3]['open']

    minimo_primera = df.iloc[0]['min']

    # La cuarta vela NO debe haber roto el mínimo de la primera
    cuarta_no_rompe = df.iloc[3]['min'] > minimo_primera

    if all([primera_roja, segunda_verde, tercera_verde, cuarta_roja, cuarta_no_rompe]):
        return True, minimo_primera

    return False, None

# ==============================
# 📉 FILTRO TENDENCIA BAJISTA
# ==============================
def tendencia_bajista(df):
    """
    Verifica que las últimas 3 velas cierren por debajo de la EMA 50.
    """
    ema = df['close'].ewm(span=50).mean()
    ultimas_velas = df.tail(3)

    for i in range(len(ultimas_velas)):
        precio = ultimas_velas.iloc[i]['close']
        ema_valor = ema.iloc[-len(ultimas_velas) + i]
        if precio >= ema_valor:
            return False

    return True

# ==============================
# 💰 ABRIR OPERACIÓN (30 SEG)
# ==============================
def abrir_operacion_put(monto):
    """
    Intenta abrir una operación PUT.
    Primero intenta opción digital (permite menor tiempo).
    Si falla, usa binaria clásica de 1 minuto (mínimo de IQ Option).
    Retorna: (estado, id_operacion, tipo)
    """
    # Intento 1: Digital (soporta expiraciones más cortas)
    try:
        estado, id_op = Iq.buy_digital_spot(ACTIVO, monto, "PUT", 1)
        if estado:
            return True, id_op, "digital"
    except Exception as e:
        print(f"⚠️ Digital falló: {e}")

    # Intento 2: Binaria clásica 1 minuto (mínimo permitido)
    try:
        estado, id_op = Iq.buy(monto, ACTIVO, "PUT", 1)
        if estado:
            return True, id_op, "binaria"
    except Exception as e:
        print(f"⚠️ Binaria falló: {e}")

    return False, None, None

# ==============================
# 📊 VERIFICAR RESULTADO
# ==============================
def verificar_resultado(id_op, tipo_op):
    """
    Verifica el resultado según el tipo de operación.
    Retorna el PnL (positivo = ganancia, negativo/0 = pérdida).
    """
    try:
        if tipo_op == "digital":
            resultado = Iq.check_win_digital_v2(id_op)
        else:
            resultado = Iq.check_win_v3(id_op)
        return resultado
    except Exception as e:
        print(f"⚠️ Error verificando resultado: {e}")
        return 0

# ==============================
# 🔄 LOOP PRINCIPAL
# ==============================
while True:
    try:
        # Reset diario
        nuevo_dia = time.strftime("%Y-%m-%d")
        if nuevo_dia != dia_actual:
            dia_actual = nuevo_dia
            operaciones_hoy = 0
            print("🔄 Nuevo día — contador reiniciado")
            enviar_telegram("🔄 Nuevo día, contador reiniciado")

        # Límite diario alcanzado
        if operaciones_hoy >= MAX_OPERACIONES_DIA:
            print("🚫 Límite diario alcanzado")
            time.sleep(10)
            continue

        segundos = int(time.strftime("%S"))

        # ✅ Solo actuar en los PRIMEROS 30 SEGUNDOS de la vela
        # (si pasamos de 30s, la quinta vela ya está muy avanzada)
        if segundos > 30:
            time.sleep(0.3)
            continue

        # Pedimos 6 velas: 4 para el patrón + 1 quinta vela en curso + 1 extra de margen
        velas = Iq.get_candles(ACTIVO, 60, 6, time.time())
        df = pd.DataFrame(velas)

        if len(df) < 5:
            print("⚠️ No hay suficientes velas")
            time.sleep(1)
            continue

        # Las 4 primeras velas son el patrón histórico (cerradas)
        df_patron = df.iloc[:4].reset_index(drop=True)

        # La quinta vela es la que está en curso (puede estar incompleta)
        vela_quinta = df.iloc[4]

        print(f"⏱ Seg: {segundos} | Chequeando patrón...")

        patron, soporte = es_patron_4velas(df_patron)

        if patron and tendencia_bajista(df):

            min_quinta = vela_quinta['min']
            print(f"🎯 Patrón detectado | Soporte: {soporte} | Min 5ta vela: {min_quinta}")

            # ✅ La quinta vela debe tocar o romper la mecha de la primera vela roja
            toca_soporte = min_quinta <= (soporte + tolerancia)

            if not toca_soporte:
                print("⏳ La quinta vela aún no toca el soporte")
                time.sleep(0.5)
                continue

            # Evitar operar en el mismo soporte dos veces
            if soporte == ultimo_soporte:
                print("⚠️ Soporte ya operado anteriormente, ignorando")
                time.sleep(1)
                continue

            # =====================
            # 💥 ENTRADA PUT
            # =====================
            print("💥 ENTRADA DETECTADA — PUT")

            monto_actual = secuencia_martingala[indice_mg]

            estado, id_op, tipo_op = abrir_operacion_put(monto_actual)

            if estado:
                operaciones_hoy += 1
                ultimo_soporte = soporte

                print(f"✅ Operación abierta | Tipo: {tipo_op} | Monto: {monto_actual} | MG nivel: {indice_mg}")

                enviar_telegram(
                    f"📥 OPERACIÓN ABIERTA\n"
                    f"Activo: {ACTIVO}\n"
                    f"Tipo: PUT 🔻\n"
                    f"Modalidad: {tipo_op}\n"
                    f"Monto: ${monto_actual}\n"
                    f"Nivel MG: {indice_mg}\n"
                    f"Soporte: {soporte}\n"
                    f"Hora: {time.strftime('%H:%M:%S')}"
                )

                # ✅ Esperar 35 segundos (30s operación + 5s margen de cierre)
                print("⏳ Esperando cierre de operación (35s)...")
                time.sleep(35)

                # Verificar resultado
                resultado = verificar_resultado(id_op, tipo_op)
                print(f"📈 Resultado PnL: {resultado}")

                if resultado > 0:
                    estado_resultado = "✅ GANADA"
                    indice_mg = 0
                    print("✅ GANADA → Reiniciar martingala")
                else:
                    estado_resultado = "❌ PERDIDA"
                    indice_mg += 1
                    print("❌ PERDIDA → Avanzar martingala")

                    if indice_mg >= len(secuencia_martingala):
                        print("🔁 Fin de secuencia → Reiniciar martingala")
                        indice_mg = 0

                enviar_telegram(
                    f"📊 RESULTADO\n"
                    f"{estado_resultado}\n"
                    f"PnL: {resultado}\n"
                    f"Siguiente nivel MG: {indice_mg}\n"
                    f"Ops hoy: {operaciones_hoy}/{MAX_OPERACIONES_DIA}"
                )

                # Pausa antes del siguiente ciclo
                time.sleep(10)

            else:
                print("❌ No se pudo abrir la operación")
                enviar_telegram("❌ Error al abrir operación (digital y binaria fallaron)")

        else:
            print(f"⏳ Sin patrón válido | Seg: {segundos}")

        time.sleep(0.5)

    except Exception as e:
        print(f"❌ Error en loop: {e}")
        enviar_telegram(f"❌ Error en bot: {e}")
        time.sleep(1)