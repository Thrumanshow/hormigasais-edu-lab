import serial, json, sys, time, hmac, hashlib

VERSION  = "1.0.0-hw"
NODE_ID  = "centinela_hw_01"
SECRET   = b"hormigasais-colonia-escuela"
PORT     = "/dev/ttyUSB0"   # Termux: ls /dev/tty* para confirmar
BAUD     = 115200

def firmar(d):
    payload = json.dumps(d, sort_keys=True).encode()
    sig = hmac.new(SECRET, payload, hashlib.sha256).hexdigest()[:16]
    d["sig"] = sig
    return json.dumps(d)

def abrir_serial():
    intentos = 0
    while intentos < 5:
        try:
            s = serial.Serial(PORT, BAUD, timeout=2)
            print(f"[HW] Puerto {PORT} abierto a {BAUD} baud.")
            return s
        except serial.SerialException as e:
            intentos += 1
            print(f"[HW] Reintento {intentos}/5 — {e}")
            time.sleep(3)
    print(f"[ERROR] No se pudo abrir {PORT}. Verifica: pkg install python-pyserial")
    sys.exit(1)

def ejecutar():
    print(f"[HormigasAIS] Centinela Hardware [{NODE_ID}] v{VERSION}")
    print(f"[HW] Escuchando ESP8266 en {PORT}...")
    print("-" * 70)
    ser = abrir_serial()
    try:
        while True:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                sys.stdout.write("* ")
                sys.stdout.flush()
                continue
            try:
                d = json.loads(linea)
            except json.JSONDecodeError:
                continue

            # Boot message del ESP
            if "boot" in d:
                print(f"\n[HW] ESP8266 conectado: {d}")
                continue

            # Evento de deteccion real
            if d.get("type") == "mosquito_pulse":
                d["origin"] = NODE_ID
                d["version"] = VERSION
                # Firmar antes de emitir al bus
                paquete = firmar(d)
                print(f"\n[ALERTA] Sensor PIR activado (I={d.get('intensity', 0):.2f})")
                print(f"[XOXO-BUS] FEROMONA_EMITIDA ==> {paquete}")
                print("[BUS] Nodos trampa alertados.")
                print("-" * 70)
                # Cooldown para no saturar
                time.sleep(4)

    except KeyboardInterrupt:
        print("\n[STOP] Centinela hardware detenido.")
    finally:
        ser.close()
        print("[HW] Puerto serial cerrado.")

if __name__ == "__main__":
    ejecutar()
