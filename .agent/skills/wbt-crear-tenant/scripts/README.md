# crear-tenant

Archivos usados por el skill "wbt-crear-tenant" para dar de alta tenants en Workbeat.

- `crear_tenant_workbeat.py`: obtiene el token OAuth y crea el tenant contra la API.
- `workbeat_config.example.json`: copia como `workbeat_config.json` para elegir el
  origen de credenciales (`"prompt"` o `"file"`).
- `workbeat_credentials.example.json`: copia como `workbeat_credentials.json` y
  coloca ahí el usuario/password real si usas `"credentials_source": "file"`.
  **No subas este archivo a ningún repositorio** — contiene un password en texto plano.
- `tenant_creation_log.jsonl`: se genera automáticamente al ejecutar el script;
  registra cada intento de creación (entrada + resultado o error).

Uso:

```bash
python crear_tenant_workbeat.py --json tenant.json
```
