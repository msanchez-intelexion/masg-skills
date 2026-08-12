---
name: "wbt-crear-tenant"
description: "Crea un tenant nuevo en Workbeat a partir de una solicitud de alta (correo/imagen con Lead, Comercial, Organización, datos del contacto, tipo de tenant y módulos). Úsala siempre que el usuario pida \"crear un tenant\", \"dar de alta un cliente en Workbeat\", \"generar el JSON de tenant\" para TRIAL/DEMO/PRODUCCIÓN, o pida ejecutar el alta contra la API de Workbeat (login.workbeat.com / shell.workbeat.com), incluso si solo mencionan \"solicito tu apoyo para la creación del tenant de X\"."
---

---
name: wbt-crear-tenant
description: Crea un tenant nuevo en Workbeat a partir de una solicitud de alta (correo/imagen con Lead, Comercial, Organización, datos del contacto, tipo de tenant y módulos). Úsala siempre que el usuario pida "crear un tenant", "dar de alta un cliente en Workbeat", "generar el JSON de tenant" para TRIAL/DEMO/PRODUCCIÓN, o pida ejecutar el alta contra la API de Workbeat (login.workbeat.com / shell.workbeat.com), incluso si solo mencionan "solicito tu apoyo para la creación del tenant de X".
---

# Crear tenant en Workbeat

Esta skill cubre el flujo completo de alta de un tenant en Workbeat: interpretar la
solicitud, armar el JSON con las reglas de negocio correctas, y (opcionalmente)
ejecutarlo contra la API real usando el script incluido.

## Dónde viven los archivos de esta skill

El script y los archivos que necesita esta skill (script de Python, plantillas de
configuración/credenciales, log y resultados) **no están dentro de la carpeta
instalada del skill**, sino en una carpeta de proyecto separada, al mismo nivel
que la carpeta donde vive este propio skill:

```
wbt-crear-tenant/
├── crear_tenant_workbeat.py
├── workbeat_config.example.json
├── workbeat_credentials.example.json
├── workbeat_config.json           (si el usuario ya lo configuró)
├── workbeat_credentials.json      (si el usuario ya lo configuró)
├── tenant_creation_log.jsonl      (se genera solo)
└── resultados/                    (se genera solo, un archivo por ejecución)
```

Antes de intentar ejecutar el script, ubica esta carpeta `wbt-crear-tenant`
(normalmente en la carpeta de trabajo/proyecto del usuario, hermana de la carpeta
de skills) y trabaja siempre dentro de ella — es decir, ejecuta el script desde
ahí (o referenciando su ruta completa) para que las rutas relativas de
configuración, log y resultados apunten al lugar correcto. Si no la encuentras,
pregúntale al usuario la ruta antes de improvisar una ubicación nueva.

## El flujo tiene tres puntos de control obligatorios

En este orden, sin saltarte ninguno ni combinarlos en un solo mensaje: el usuario
necesita ver y validar el JSON antes de que se ejecute cualquier llamada real a
la API, porque crear un tenant en producción no es reversible con un solo clic.

### Punto de control 1: Reunir la información de la solicitud

Antes de generar nada, confirma que tienes todos los datos necesarios de la
solicitud (texto, correo o imagen): Lead, Comercial, Organización, Nombre,
ApellidoPaterno, ApellidoMaterno, Posición, Teléfono, y si se trata de TRIAL,
DEMO, HRC/Corporate o una solicitud normal de producción.

- Si falta algún dato imprescindible para decidir las reglas (por ejemplo no
  queda claro si es TRIAL/DEMO/producción, o el dominio del cliente para un
  TRIAL), pregúntalo antes de continuar en vez de asumir.
- **Teléfono** es el único campo con fallback automático: si no viene en la
  solicitud, genera uno sintético de 10 dígitos (por ejemplo prefijo 81 + 8
  dígitos aleatorios) y dilo explícitamente al mostrar el JSON, para que quede
  claro que no vino del cliente.
- **Comercial siempre debe tener dominio @intelexion.com** (es un vendedor
  interno de Intelexion, nunca del cliente). Si la solicitud trae un correo de
  Comercial con otro dominio, o el dato viene incompleto/dudoso, no lo asumas ni
  lo corrijas por tu cuenta: pregúntale al usuario cuál es el correo correcto de
  Intelexion antes de continuar. Esta regla es solo para **Comercial** — el
  **Lead** sigue las reglas de dominio de la sección siguiente (normalmente el
  dominio del cliente, salvo el caso especial de TRIAL descrito ahí).

### Punto de control 2: Generar y mostrar el JSON completo al usuario

Arma el JSON con esta plantilla:

```json
{
  "Lead": "",
  "Comercial": "",
  "Organizacion": "",
  "Nombre": "",
  "ApellidoPaterno": "",
  "ApellidoMaterno": "",
  "Posicion": "",
  "Telefono": "",
  "Modulos": "",
  "TipoTenant": "",
  "DiasVigencia": "",
  "Estatus": ""
}
```

Reglas para llenarlo:

- **TipoTenant / DiasVigencia / Estatus se calculan siempre con estas reglas de
  negocio, sin importar qué valores traiga la solicitud/imagen para estos tres
  campos.** Si el material recibido ya trae, por ejemplo, `"TipoTenant": "PROD"`,
  `"DiasVigencia": "365"` o cualquier otro valor explícito, ignóralo y usa el que
  corresponda según la clasificación de la solicitud (TRIAL / DEMO / HRC-Corporate
  / producción normal) descrita abajo. Estos tres campos nunca se copian tal cual
  de la fuente.
  - **TRIAL**: `"TipoTenant": "TRIAL"`, `"DiasVigencia": "60"`, `"Estatus": "PRUEBA"`.
    Además, el `Lead` se arma como `admin.workshop@<dominio-del-cliente>`, tomando
    el dominio del correo del cliente recibido (nunca un dominio genérico como
    gmail.com, hotmail.com u outlook.com — si el correo recibido es genérico,
    pregunta al usuario por el dominio corporativo real).
  - **DEMO**: `"TipoTenant": "DEMO"`, `"DiasVigencia": "30"`, `"Estatus": "PRUEBA"`.
  - **Producción / solicitud normal** (no mencionan trial ni demo): siempre
    `"TipoTenant": "COMPRA"`, `"DiasVigencia": "366"`, `"Estatus": "PRODUCCIÓN"`.
  - Si la solicitud viene de `hbarajas@intelexion.com`, o mencionan que es para
    **HRC** o **Corporate**, sobrescribe:
    `"Comercial": "hbarajas@intelexion.com"`, `"Modulos": "ADM|ORG|CRH|NOM|CFDI"`.

- **Modulos**: NUNCA copies tal cual la lista de módulos que venga en la imagen o
  correo del cliente. Los módulos siempre se recalculan con estas reglas fijas:

  | Caso | Modulos |
  |---|---|
  | DEMO | `CORERH\|CRH\|ASI2\|VAC\|NOM2\|CFDI\|SAT\|EV360\|BDT\|CLI\|CAP\|DIA\|DES\|REC\|MED` |
  | TRIAL | `ADM\|ORG\|CRH\|ASI2\|VAC\|NOM2\|CFDI\|SAT\|EV360\|BDT\|CLI\|CAP\|DIA\|DES\|REC\|MED` |
  | Producción, "todo RH" / Workbeat Care (llevan asistencia, vacaciones, nómina, y módulos de RH como evaluación 360, capacitación, desarrollo, reclutamiento, etc.) | `ADM\|ORG\|CRH\|ASI2\|VAC\|NOM2\|CFDI\|SAT\|EV360\|BDT\|CLI\|CAP\|DIA\|DES\|REC\|MED` |
  | Producción, Workbeat Pro (llevan nómina + vacaciones o asistencia, pero no llevan los módulos de RH completos) | `ADM\|ORG\|CRH\|ASI2\|VAC\|NOM2\|CFDI\|SAT` |
  | Producción, Workbeat Pay (no llevan asistencia ni vacaciones, solo nómina) | `ADM\|ORG\|CRH\|NOM2\|CFDI\|SAT` |
  | HRC / Corporate | `ADM\|ORG\|CRH\|NOM\|CFDI` |

  Usa la solicitud original solo para decidir cuál fila de la tabla aplica (por
  ejemplo, si menciona evaluación 360 / capacitación / diagnóstico / desarrollo /
  reclutamiento, o si trae los mismos módulos que la tabla de Care, es Workbeat
  Care). No mezcles variantes de nombres de módulo (por ejemplo `ASI` vs `ASI2`,
  `NOM` vs `NOM2`) — usa siempre la variante exacta de la fila que aplica.

Muestra el JSON completo y legible en tu respuesta (bloque ```json```), señalando
cualquier dato que hayas inferido, generado o recalculado en lugar de tomar tal
cual de la fuente (teléfono sintético, dominio del Lead en TRIAL, TipoTenant /
DiasVigencia / Estatus recalculados, Módulos recalculados). Termina este mensaje
preguntando explícitamente si el JSON es correcto y si quieres que proceda a
ejecutarlo contra la API real. **No avances al punto de control 3 en el mismo
turno** — espera la respuesta del usuario.

### Punto de control 3: Confirmación explícita antes de ejecutar

Solo ejecuta el script `crear_tenant_workbeat.py` contra la API real después de
que el usuario haya confirmado explícitamente (por ejemplo "sí", "adelante",
"confirmado", o pidió una corrección y luego confirmó el JSON corregido). Una
petición inicial como "crea el tenant" o "dame el JSON" no cuenta como esa
confirmación — es la señal para llegar hasta el punto de control 2 y detenerte
ahí a esperar el visto bueno.

Si el usuario corrige algo del JSON, regenera el JSON actualizado, muéstralo de
nuevo, y vuelve a pedir confirmación antes de ejecutar.

Una vez confirmado, ejecuta (desde la carpeta `wbt-crear-tenant`, o referenciando
su ruta completa):

```bash
python crear_tenant_workbeat.py --json tenant.json
```

Este script:

1. Obtiene usuario y password (en pantalla o desde un archivo de credenciales,
   ver más abajo).
2. Pide un token OAuth a `https://login.workbeat.com/connect/token`.
3. Crea el tenant con `POST https://shell.workbeat.com/api/HR/Invitation`,
   mandando el JSON confirmado y el token como `Authorization: Bearer`.
4. Guarda el resultado de la ejecución en dos lugares dentro de la misma carpeta
   `wbt-crear-tenant`:
   - Agrega una línea al log acumulado `tenant_creation_log.jsonl` (historial
     completo de todas las ejecuciones).
   - Crea un archivo individual dentro de la subcarpeta `resultados/` (por
     ejemplo `resultados/20260731_120000_graco_mexicana.json`), con el JSON de
     entrada y el resultado o error de esa ejecución puntual. Esta subcarpeta se
     crea automáticamente si no existe — no necesitas crearla tú.

Si el usuario ya tiene credenciales guardadas, el script las toma automáticamente
según `workbeat_config.json` (ver `workbeat_config.example.json` en esta carpeta
para el formato). Si no hay configuración, el script pregunta usuario y password
en pantalla (password oculto).

### Dónde vive el archivo de credenciales

El archivo real de credenciales (`workbeat_credentials.json`) debe colocarse en
esta misma carpeta `wbt-crear-tenant` (junto al script), NUNCA compartido ni
subido a un repositorio. Usa `workbeat_credentials.example.json` como plantilla
de formato. Como contiene un password en texto plano, sugiere al usuario
restringir permisos del archivo o preferir el modo interactivo
(`"credentials_source": "prompt"`) si el entorno es compartido.

## Después de ejecutar

Reporta al usuario el resultado que devolvió la API (éxito o el error recibido),
y dile en qué archivo de `resultados/` quedó guardado ese resultado específico
(además de que también se agregó al log acumulado `tenant_creation_log.jsonl`)
para trazabilidad.

