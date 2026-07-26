import subprocess, json, sys, time, threading

VERSION = "0.3.0"

def reporter(trampa_ref, intervalo=30):
    while True:
        time.sleep(intervalo)
        estado = "ACTIVO" if trampa_ref.activo else "LETARGO"
        print(f"\n[REPORTE] Capturas={trampa_ref.total_capturas} | "
              f"Estado={estado} | Temp={trampa_ref.temperatura}C")

def iniciar_colonia():
    print(f"[HormigasAIS] Colonia Nodo Escuela v{VERSION}")
    print("[BUS] Acoplando subprocesos y cargando contratos...")
    print("-" * 70)

    try:
        from hormiga_trampa import HormigaTrampa
        trampa = HormigaTrampa()
    except ImportError:
        print("[ERROR] Falta hormiga_trampa.py")
        return

    threading.Thread(
        target=reporter, args=(trampa, 30), daemon=True
    ).start()

    proceso = subprocess.Popen(
        ["python3", "hormiga_centinela.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        for linea in iter(proceso.stdout.readline, ""):
            linea = linea.strip()
            if "FEROMONA_EMITIDA ==>" in linea:
                partes = linea.split("==>")
                if len(partes) > 1:
                    trampa.escuchar_bus(partes[1].strip())
            elif "*" in linea:
                sys.stdout.write("* ")
                sys.stdout.flush()
                trampa.escuchar_bus('{"type":"env_clear"}')
    except KeyboardInterrupt:
        print("\n\n[INTERRUPCION] Apagado manual detectado.")
    except Exception as e:
        print(f"\n[FALLO BUS] Anomalia: {e}")
    finally:
        print("\n[FAILSAFE] Protocolo de desconexion segura...")
        proceso.terminate()
        trampa.apagado_seguro()
        print("[OK] Colonia cerrada de forma soberana.")

if __name__ == "__main__":
    iniciar_colonia()
