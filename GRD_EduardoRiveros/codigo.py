#!/usr/bin/env python3
"""
Wait for a remote network service to come online.
Compatible with Python 3.13.9+
"""

import argparse
import socket
import time


# ===============================
# Configuración por defecto
# ===============================
DEFAULT_TIMEOUT = 120          # Tiempo máximo de espera en segundos
DEFAULT_SERVER_HOST = 'google.com'
DEFAULT_SERVER_PORT = 443


# ===============================
# Clase principal
# ===============================
class NetServiceChecker:
    """Esperar a que un servicio de red esté disponible"""

    def __init__(self, host: str, port: int, timeout: int = DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def end_wait(self):
        """Cerrar el socket"""
        try:
            self.sock.close()
        except Exception:
            pass

    def check(self) -> bool:
        """Comprobar si el servicio de red está disponible"""
        if self.timeout:
            end_time = time.time() + self.timeout

        while True:
            try:
                if self.timeout:
                    next_timeout = end_time - time.time()
                    if next_timeout < 0:
                        print("⏰ Tiempo de espera agotado. El servicio no está disponible.")
                        return False

                    print(f"🔄 Estableciendo timeout del socket en {round(next_timeout, 2)}s")
                    self.sock.settimeout(next_timeout)

                # Intentar conectar
                self.sock.connect((self.host, self.port))

            except socket.timeout:
                print("⚠️  Tiempo de espera del socket alcanzado: el servicio aún no está disponible.")
                return False

            except socket.error as err:
                print(f"❌ Error de conexión: {err}")
                time.sleep(2)  # Esperar 2 segundos antes de volver a intentar
                continue

            else:
                # Si la conexión tiene éxito
                self.end_wait()
                return True


# ===============================
# Bloque principal
# ===============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Esperar por un servicio de red")
    parser.add_argument("--host", action="store", dest="host",
                        default=DEFAULT_SERVER_HOST,
                        help="Dirección del host (por defecto: localhost)")
    parser.add_argument("--port", action="store", dest="port", type=int,
                        default=DEFAULT_SERVER_PORT,
                        help="Puerto del servicio (por defecto: 80)")
    parser.add_argument("--timeout", action="store", dest="timeout", type=int,
                        default=DEFAULT_TIMEOUT,
                        help="Tiempo máximo de espera en segundos (por defecto: 120)")

    args = parser.parse_args()

    host, port, timeout = args.host, args.port, args.timeout

    service_checker = NetServiceChecker(host, port, timeout=timeout)

    print(f"🔍 Comprobando servicio de red {host}:{port} ...")

    if service_checker.check():
        print("✅ ¡El servicio está disponible!")
    else:
        print("❌ El servicio no se activó dentro del tiempo especificado.")

