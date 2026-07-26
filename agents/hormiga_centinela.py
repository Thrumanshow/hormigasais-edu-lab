import time, json, random, sys, hmac, hashlib

VERSION   = "0.3.0"
NODE_ID   = "centinela_escuela_01"
TARGET    = "mosquito_pulse"
SECRET    = b"hormigasais-colonia-escuela"

class UmbralAdaptativo:
    def __init__(self, base=0.75, ventana=20):
        self.historial = []
        self.base      = base
        self.ventana   = ventana

    def actualizar(self, v):
        self.historial.append(v)
        if len(self.historial) > self.ventana:
            self.historial.pop(0)

    @property
    def umbral(self):
        if len(self.historial) < 5:
            return self.base
        media = sum(self.historial) / len(self.historial)
        return round(min(media + 0.15, 0.92), 3)

def firmar(paquete_dict):
    payload = json.dumps(paquete_dict, sort_keys=True).encode()
    sig     = hmac.new(SECRET, payload, hashlib.sha256).hexdigest()[:16]
    paquete_dict["sig"] = sig
    return json.dumps(paquete_dict)

def generar_feromona(intensidad):
    p = {
        "timestamp": round(time.time(), 6),
        "type":      TARGET,
        "origin":    NODE_ID,
        "status":    "active",
        "intensity": round(intensidad, 2),
        "version":   VERSION,
    }
    return firmar(p)

def ejecutar():
    ua = UmbralAdaptativo()
    print(f"[HormigasAIS] Centinela [{NODE_ID}] v{VERSION}")
    print(f"Escaneando espectro infrarrojo... Ctrl+C para detener.")
    print("-" * 70)
    try:
        while True:
            lectura = random.uniform(0.1, 1.0)
            ua.actualizar(lectura)
            if lectura > ua.umbral:
                print(f"[ALERTA] Gradiente={round(lectura,2)} Umbral={ua.umbral}")
                paquete = generar_feromona(lectura)
                print(f"[XOXO-BUS] FEROMONA_EMITIDA ==> {paquete}")
                print("[BUS] Nodos trampa alertados.")
                print("-" * 70)
                time.sleep(5)
            else:
                sys.stdout.write("* ")
                sys.stdout.flush()
                time.sleep(1.5)
    except KeyboardInterrupt:
        print("\n[STOP] Centinela detenido. Modo letargo.")

if __name__ == "__main__":
    ejecutar()
