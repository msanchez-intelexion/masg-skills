#!/usr/bin/env python3
"""
crear_tenant_workbeat.py

Script para que un skill cree un tenant en Workbeat:
1. Obtiene usuario y password: en pantalla (interactivo) o desde un archivo de
   credenciales, según configuración.
2. Obtiene un token OAuth (POST https://login.workbeat.com/connect/token).
3. Con el token (Bearer), crea el tenant (POST https://shell.workbeat.com/api/HR/Invitation)
   enviando el JSON con los datos del tenant generado previamente con las reglas de negocio.
4. Guarda en un log (JSON Lines) el JSON de entrada y el resultado de la llamada,
   además de informar al usuario en pantalla durante la ejecución.

--------------------------------------------------------------------------------
CONFIGURACIÓN DE CREDENCIALES
--------------------------------------------------------------------------------
El origen de usuario/password se controla con un archivo de configuración
(por defecto "workbeat_config.json", en el mismo directorio que este script):

    {
      "credentials_source": "file",          // "prompt" o "file"
      "credentials_file": "workbeat_credentials.json",
      "results_dir": ""                      // opcional, ver sección de resultados abajo
    }

- "credentials_source": "prompt"  -> se solicitan en pantalla (password oculto con getpass).
- "credentials_source": "file"    -> se leen del archivo indicado en "credentials_file"
  (ruta relativa al mismo directorio del script, o ruta absoluta).
- "results_dir" (opcional) -> ruta donde guardar los archivos individuales de
  resultado (ver sección "LOG Y ARCHIVOS DE SALIDA"). Si se omite o queda
  vacío, se usa el default automático.

El archivo de credenciales ("workbeat_credentials.json" por defecto) debe tener
este formato:

    {
      "username": "admin@wbtworkshops.com",
      "password": "ltxwbt123.4"
    }

UBICACIÓN RECOMENDADA del archivo de credenciales:
- Debe vivir junto a este script (misma carpeta), NUNCA dentro de una carpeta
  que se comparta o suba a un repositorio público.
- Al contener un password en texto plano, se recomienda restringir permisos
  del archivo (en Linux/Mac: chmod 600 workbeat_credentials.json) y excluirlo
  de git (.gitignore).
- Si el skill corre en un entorno compartido, es preferible usar
  "credentials_source": "prompt" o inyectar el archivo solo en tiempo de
  ejecución (por ejemplo, un volumen/secreto montado por el orquestador).

--------------------------------------------------------------------------------
LOG Y ARCHIVOS DE SALIDA
--------------------------------------------------------------------------------
Cada ejecución queda registrada en dos lugares:
- "tenant_creation_log.jsonl": una línea (JSON) por ejecución, con timestamp,
  input (json enviado), resultado/éxito o error. Útil para ver el historial
  completo de una sola vez. Vive junto a este script.
- "<carpeta_resultados>/<timestamp>_<organizacion>.json": un archivo individual
  por ejecución con el mismo contenido, para que cada alta de tenant quede como
  su propio archivo de salida fácil de ubicar y compartir. Esta carpeta se crea
  automáticamente si no existe.

  Por default, "<carpeta_resultados>" es "resultado/" un nivel arriba de la
  carpeta ".agent" del proyecto (es decir, hermana de ".agent", no dentro de
  la skill) — así los resultados quedan fuera de la carpeta de skills, fáciles
  de encontrar y de excluir de lo que se empaqueta/instala como skill. Si el
  script no logra ubicar una carpeta ".agent" en alguna carpeta superior (por
  ejemplo si se instaló fuera de un proyecto con esa estructura), usa como
  respaldo "resultados/" junto al propio script. También se puede fijar una
  ruta explícita con "results_dir" en el archivo de configuración
  (workbeat_config.json), que tiene prioridad sobre ambas.

Uso:
    python crear_tenant_workbeat.py --json tenant.json
    python crear_tenant_workbeat.py --json tenant.json --username admin@wbtworkshops.com --password ltxwbt.1
    python crear_tenant_workbeat.py --json tenant.json --config workbeat_config.json

También puede usarse como módulo:
    from crear_tenant_workbeat import crear_tenant
    resultado = crear_tenant(username, password, tenant_dict)
"""

import argparse
import getpass
import json
import os
import sys
from datetime import datetime, timezone

import requests

# --- Configuración fija de la API de token (imagen 1 e imagen 2) ---
TOKEN_URL = "https://login.workbeat.com/connect/token"
TENANT_URL = "https://shell.workbeat.com/api/HR/Invitation"

CLIENT_ID = "oauth:flextend"
CLIENT_SECRET = "afe94888-055b-4167-be03-3ae8c44bb26c"
SCOPE = "api1 offline_access"
GRANT_TYPE = "password"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "workbeat_config.json")
DEFAULT_CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "workbeat_credentials.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "tenant_creation_log.jsonl")


def _encontrar_carpeta_proyecto(desde: str):
    """
    Busca hacia arriba, a partir de 'desde', una carpeta ".agent" y devuelve la
    carpeta que la contiene (la raíz del proyecto, un nivel arriba de ".agent").
    Si no encuentra ninguna, devuelve None.
    """
    actual = os.path.abspath(desde)
    while True:
        if os.path.basename(actual) == ".agent":
            return os.path.dirname(actual)
        padre = os.path.dirname(actual)
        if padre == actual:
            return None
        actual = padre


# Por default, los resultados se guardan en "resultado/" un nivel arriba de la
# carpeta ".agent" (fuera de la carpeta de la skill). Si no se encuentra ".agent"
# en ningún nivel superior, se usa "resultados/" junto al script como respaldo.
_PROJECT_ROOT = _encontrar_carpeta_proyecto(SCRIPT_DIR)
if _PROJECT_ROOT:
    DEFAULT_RESULTS_DIR = os.path.join(_PROJECT_ROOT, "resultado")
else:
    DEFAULT_RESULTS_DIR = os.path.join(SCRIPT_DIR, "resultados")

RESULTS_DIR = DEFAULT_RESULTS_DIR


def _resolver_ruta(ruta: str) -> str:
    """Si la ruta es relativa, la resuelve respecto al directorio del script."""
    if os.path.isabs(ruta):
        return ruta
    return os.path.join(SCRIPT_DIR, ruta)


def cargar_config(config_path: str = DEFAULT_CONFIG_FILE) -> dict:
    """Lee la configuración de origen de credenciales. Si no existe, usa 'prompt'."""
    global RESULTS_DIR

    if not os.path.exists(config_path):
        return {"credentials_source": "prompt", "credentials_file": DEFAULT_CREDENTIALS_FILE}

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config.setdefault("credentials_source", "prompt")
    config["credentials_file"] = _resolver_ruta(config.get("credentials_file", "workbeat_credentials.json"))

    # "results_dir" en la config, si viene, tiene prioridad sobre el default
    # calculado (resultado/ un nivel arriba de .agent, o resultados/ de respaldo).
    if config.get("results_dir"):
        RESULTS_DIR = _resolver_ruta(config["results_dir"])
    config["results_dir"] = RESULTS_DIR

    return config


def obtener_credenciales(config: dict, username_arg: str = None, password_arg: str = None) -> tuple:
    """
    Resuelve usuario/password en este orden de prioridad:
    1. Argumentos explícitos (--username/--password).
    2. Archivo de credenciales, si credentials_source == "file".
    3. Solicitud interactiva en pantalla (default).
    """
    if username_arg and password_arg:
        return username_arg, password_arg

    if config.get("credentials_source") == "file":
        creds_path = config["credentials_file"]
        if not os.path.exists(creds_path):
            raise FileNotFoundError(
                f"No se encontró el archivo de credenciales: {creds_path}"
            )
        with open(creds_path, "r", encoding="utf-8") as f:
            creds = json.load(f)
        username = username_arg or creds.get("username")
        password = password_arg or creds.get("password")
        if not username or not password:
            raise ValueError(f"El archivo {creds_path} no contiene 'username'/'password' válidos.")
        print(f"[INFO] Credenciales leídas desde archivo: {creds_path}")
        return username, password

    # Fallback: modo interactivo
    username = username_arg or input("Usuario: ")
    password = password_arg or getpass.getpass("Password: ")
    return username, password


def obtener_token(username: str, password: str) -> str:
    """Solicita el token OAuth usando usuario y password del cliente."""
    payload = {
        "grant_type": GRANT_TYPE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
        "username": username,
        "password": password,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print(f"[INFO] Solicitando token a {TOKEN_URL} ...")
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError(f"No se recibió access_token en la respuesta: {data}")

    print("[INFO] Token obtenido correctamente.")
    return access_token


def crear_tenant_api(token: str, tenant_json: dict) -> dict:
    """Crea el tenant llamando al API de Invitation con el Bearer token."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    print(f"[INFO] Creando tenant en {TENANT_URL} ...")
    response = requests.post(TENANT_URL, json=tenant_json, headers=headers)
    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        return {"status_code": response.status_code, "text": response.text}


def _slug(texto: str) -> str:
    """Convierte un texto libre en un slug simple apto para nombre de archivo."""
    if not texto:
        return "tenant"
    slug = "".join(c if c.isalnum() else "_" for c in texto.strip())
    slug = "_".join(filter(None, slug.split("_")))
    return slug[:60] or "tenant"


def registrar_log(tenant_json: dict, resultado: dict = None, error: str = None):
    """
    Registra el resultado de una ejecución en dos lugares:
    1. Agrega una línea al log acumulado (JSONL) "tenant_creation_log.jsonl".
    2. Guarda un archivo de salida individual en la carpeta "resultados/" con el
       JSON de entrada y el resultado/error de esa ejecución puntual, para que
       cada alta quede como un archivo propio y fácil de ubicar.
    """
    timestamp = datetime.now(timezone.utc)
    entrada = {
        "timestamp": timestamp.isoformat(),
        "input": tenant_json,
        "resultado": resultado,
        "error": error,
        "estado": "OK" if error is None else "ERROR",
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
    print(f"[INFO] Log actualizado en: {LOG_FILE}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    organizacion = _slug(tenant_json.get("Organizacion", ""))
    nombre_archivo = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{organizacion}.json"
    ruta_resultado = os.path.join(RESULTS_DIR, nombre_archivo)
    with open(ruta_resultado, "w", encoding="utf-8") as f:
        json.dump(entrada, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Resultado de esta ejecución guardado en: {ruta_resultado}")


def crear_tenant(username: str, password: str, tenant_json: dict) -> dict:
    """Flujo completo: obtiene token, crea el tenant y registra el log. Retorna la respuesta del API."""
    try:
        token = obtener_token(username, password)
        resultado = crear_tenant_api(token, tenant_json)
        registrar_log(tenant_json, resultado=resultado)
        print("[INFO] Tenant creado y registrado en el log correctamente.")
        return resultado
    except requests.HTTPError as e:
        error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
        registrar_log(tenant_json, error=error_msg)
        raise
    except Exception as e:
        registrar_log(tenant_json, error=str(e))
        raise


def main():
    parser = argparse.ArgumentParser(description="Crea un tenant en Workbeat.")
    parser.add_argument("--json", required=True, help="Ruta al archivo JSON con los datos del tenant.")
    parser.add_argument("--username", help="Usuario para autenticarse (opcional, tiene prioridad sobre config/archivo).")
    parser.add_argument("--password", help="Password para autenticarse (opcional, tiene prioridad sobre config/archivo).")
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_FILE,
        help=f"Ruta al archivo de configuración de credenciales (default: {DEFAULT_CONFIG_FILE}).",
    )
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        tenant_json = json.load(f)

    config = cargar_config(args.config)

    try:
        username, password = obtener_credenciales(config, args.username, args.password)
        resultado = crear_tenant(username, password, tenant_json)
    except requests.HTTPError as e:
        print(f"[ERROR] Error HTTP: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
