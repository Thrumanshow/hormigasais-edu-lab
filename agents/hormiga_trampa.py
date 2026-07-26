import time, json, hmac, hashlib

VERSION          = "0.3.0"
NODE_ID          = "trampa_escuela_01"
TRIGGER_TYPE     = "mosquito_pulse"
CICLOS_GRACIA    = 4
SECRET           = b"hormigasais-colonia-escuela"
LOG_FILE         = "capturas.jsonl"

class HormigaTrampa:
    def __init__(self):
        self.activo              = False
        self.temperatura         = 24.0
        self.ciclos_sin_feromona = 0
        self.total_capturas      = 0
        self._ultimo_ts          = 0.0   # anti-duplicado

    # ── Verificación HMAC ──────────────────────────────────────────────
    def _verificar(self, d):
        sig_rx = d.pop("sig", "")
        payload = json.dumps(d, sort_keys=True).encode()
        sig_ok  = hmac.new(SECRET, payload, hashlib.sha256).hexdigest()[:16]
        d["sig"] = sig_rx          # restaurar para no mutar el dict
        return hmac.compare_digest(sig_rx, sig_ok)

    # ── Registro soberano ──────────────────────────────────────────────
    def _registrar(self, intensidad):
        entrada = {
            "ts":        round(time.time(), 3),
            "node":      NODE_ID,
            "intensidad": intensidad,
            "succion":   "MAX" if intensidad > 0.85 else "MOD",
        }
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entrada) + "\n")

    # ── Bus principal ──────────────────────────────────────────────────
    def escuchar_bus(self, paquete_crudo):
        try:
            d = json.loads(paquete_crudo)
        except Exception:
            return

        if d.get("type") == TRIGGER_TYPE and d.get("status") == "active":
            # Anti-duplicado: ignorar si mismo timestamp ya procesado
            ts = d.get("timestamp", 0)
            if ts == self._ultimo_ts:
                return
            self._ultimo_ts = ts

            if not self._verificar(dict(d)):
                print(f"[SEGURIDAD] Firma invalida — paquete descartado.")
                return

            self.ciclos_sin_feromona = 0
            self.reaccionar(d.get("intensity", 0.5))
        else:
            self.evaluar_disipacion()

    # ── Reacción ───────────────────────────────────────────────────────
    def reaccionar(self, intensidad):
        self.activo      = True
        self.temperatura = 36.5
        self.total_capturas += 1
        succion = "100% (MAXIMA)" if intensidad > 0.85 else "60% (MODERADA)"

        print(f"\n[{NODE_ID}] Feromona detectada (I={intensidad} | Captura #{self.total_capturas})")
        print(f"[ACTUADOR] Resistencia IR -> {self.temperatura}C")
        print(f"[MECANICO] Extractor al {succion}")
        print("-" * 65)
        self._registrar(intensidad)

    # ── Disipación ─────────────────────────────────────────────────────
    def evaluar_disipacion(self):
        if not self.activo:
            return
        self.ciclos_sin_feromona += 1
        restantes = CICLOS_GRACIA - self.ciclos_sin_feromona
        if restantes > 0:
            print(f"\n[{NODE_ID}] Silencio. Persistencia biologica ({restantes} ciclos)...")
            print(f"[ACTUADOR] Manteniendo gradiente a {self.temperatura}C")
            print("-" * 65)
        else:
            print(f"\n[{NODE_ID}] Feromona evaporada.")
            self.apagado_seguro()

    # ── Apagado ────────────────────────────────────────────────────────
    def apagado_seguro(self):
        if self.activo:
            self.temperatura = 24.0
            self.activo      = False
            print("[BAJO CONSUMO] Extractor OFF. IR -> 24C. Modo letargo.")
            print(f"[STATS] Total capturas esta sesion: {self.total_capturas}")
            print("-" * 65)
