---
name: "wbt-crear-tenant"
description: "Crea un tenant nuevo en Workbeat a partir de una solicitud de alta (correo/imagen con Lead, Comercial, Organización, datos del contacto, tipo de tenant y módulos). Úsala siempre que el usuario pida \"crear un tenant\", \"dar de alta un cliente en Workbeat\", \"generar el JSON de tenant\" para TRIAL/DEMO/PRODUCCIÓN, o pida ejecutar el alta contra la API de Workbeat (login.workbeat.com / shell.workbeat.com), incluso si solo mencionan \"solicito tu apoyo para la creación del tenant de X\"." 
---

# Crear tenant en Workbeat

Esta skill cubre el flujo completo de alta de un tenant en Workbeat: interpretar la
solicitud, armar el JSON con las reglas de negocio correctas, y (opcionalmente)
ejecutarlo contra la API real usando el script incluido. 

## Dónde vive el script (siempre en el mismo lugar, dentro de esta skill)

El script de Python y todo lo que necesita (plantillas de configuración/credenciales,
credenciales reales si el usuario ya las configuró, y log acumulado) viven **dentro de
esta misma skill**, en la subcarpeta `scripts/`, justo al lado de este archivo
`SKILL.md`. Los **resultados individuales de cada ejecución son la única excepción**:
el propio script los guarda fuera de la skill, en una carpeta `resultado/` un nivel
arriba de `.agent` (es decir, en la raíz del proyecto, hermana de `.agent`):

```
<raíz del proyecto>/
├── .agent/
│   └── skills/
│       └── wbt-crear-tenant/              (carpeta de esta skill)
│           ├── SKILL.md
│           └── scripts/
│               ├── crear_tenant_workbeat.py
│               ├── workbeat_config.example.json
│               ├── workbeat_config.json           (si el usuario ya lo configuró)
│               ├── workbeat_credentials.example.json
│               ├── workbeat_credentials.json      (si el usuario ya lo configuró; nunca compartir ni subir a un repo)
│               └── tenant_creation_log.jsonl       (se genera solo — log acumulado, junto al script)
└── resultado/                             (se genera solo — un archivo por ejecución, FUERA de .agent)
```

El propio script resuelve la ruta del script y la del log relativas a su propia
ubicación (no al directorio desde el que se invoque), así que **no hace falta buscar ni
adivinar ninguna carpeta de proyecto para eso**: usa siempre la ruta
`scripts/crear_tenant_workbeat.py` dentro de la carpeta de esta skill (la misma carpeta
donde está este `SKILL.md`). Si por alguna razón esa subcarpeta `scripts/` no existe o
el script no está ahí, dilo explícitamente y pregunta al usuario en lugar de improvisar
otra ubicación.

Para la carpeta de resultados sí hay una búsqueda automática, pero la hace el propio
script (no tienes que calcularla tú): busca hacia arriba desde su propia ubicación hasta
encontrar una carpeta `.agent`, y usa la carpeta que la contiene + `resultado/` como
destino. Si no encuentra ninguna `.agent` en los niveles superiores (por ejemplo, si la
skill se instaló fuera de un proyecto con esa estructura), cae de respaldo a
`scripts/resultados/` junto al script. También se puede fijar una ruta explícita con la
clave `"results_dir"` en `workbeat_config.json`, que tiene prioridad sobre ambas.

## Configuración inicial (solo la primera vez que se usa esta skill en un equipo)

Antes de pedir datos de ningún tenant, revisa si ya existe
`scripts/workbeat_config.json` dentro de esta skill.

- **Si ya existe**, no preguntes nada de esta sección — usa la configuración tal
  cual está y pasa directo al punto de control 1.
- **Si no existe** (primera vez que se usa esta skill en este equipo), antes de
  continuar pregúntale al usuario, en un solo mensaje, estas dos cosas:

  1. **Guardar credenciales o pedirlas cada vez.** Pregunta algo como: "¿Quieres
     que guarde tu usuario y contraseña de Workbeat en este equipo para no
     pedírtelos cada vez que creemos un tenant, o prefieres que te los pida cada
     vez?"
     - Si responde que los guarde: pídele usuario y password, y crea
       `scripts/workbeat_credentials.json` con
       `{"username": "...", "password": "..."}` (formato en
       `scripts/workbeat_credentials.example.json`). Adviértele explícitamente
       que ese archivo queda en texto plano en su equipo, que nunca debe
       compartirse ni subirse a un repositorio, y confirma que el proyecto ya
       lo excluye de git si tiene un `.gitignore` con esa regla (si no lo tiene,
       sugiérele agregarlo).
     - Si responde que prefiere que se los pidas cada vez: no crees
       `workbeat_credentials.json`. En este caso, en el punto de control 3, tú
       (el agente) le pides usuario y password en el chat en el momento de
       ejecutar — nunca uses el modo interactivo del script para esto (ver nota
       más abajo), y nunca guardes esas credenciales en ningún archivo.
  2. **Dónde guardar los resultados.** Explica el default automático (carpeta
     `resultado/` un nivel arriba de `.agent`, ver sección anterior) y pregúntale
     si lo quiere así o si prefiere otra ruta. Si pide otra ruta, esa va en la
     clave `"results_dir"` de `workbeat_config.json`; si acepta el default, deja
     `"results_dir"` vacío o sin esa clave.

  Con las dos respuestas, crea `scripts/workbeat_config.json`:

  ```json
  {
    "credentials_source": "file",            // "file" si eligió guardarlas, "prompt" si prefiere que se le pidan cada vez
    "credentials_file": "workbeat_credentials.json",
    "results_dir": ""                        // ruta elegida, o vacío para el default automático
  }
  ```

  Confírmale al usuario qué quedó configurado (dónde guardaste o no las
  credenciales, y qué carpeta de resultados va a usar) antes de seguir con el
  punto de control 1.

**Nota importante sobre `"credentials_source": "prompt"`:** ese valor le indica
al *script* que pida usuario/password de forma interactiva (oculto en pantalla)
si se ejecuta desde una terminal normal. Pero cuando tú ejecutas el script como
agente (por ejemplo con la herramienta de shell), no hay una terminal
interactiva real, así que ese prompt no va a funcionar. Por eso, si la
configuración quedó en `"prompt"`, eres tú quien debe pedir usuario y password
en el chat (en el punto de control 3, justo antes de ejecutar) y pasarlos como
`--username` y `--password` al invocar el script — nunca dependas de que el
script los pida solo.

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

Una vez confirmado, revisa `scripts/workbeat_config.json` (creado en la
configuración inicial):

- Si `"credentials_source": "file"` → no necesitas pedir nada, el script toma
  las credenciales de `workbeat_credentials.json` automáticamente. Ejecuta:

  ```bash
  python scripts/crear_tenant_workbeat.py --json tenant.json
  ```

- Si `"credentials_source": "prompt"` → pídele al usuario, en el chat, su
  usuario y password de Workbeat en este mismo momento (justo antes de
  ejecutar), y pásalos como argumentos (nunca los guardes en ningún archivo):

  ```bash
  python scripts/crear_tenant_workbeat.py --json tenant.json --username "correo@dominio.com" --password "la_password"
  ```

Este script:

1. Obtiene usuario y password (en pantalla o desde un archivo de credenciales,
   ver más abajo).
2. Pide un token OAuth a `https://login.workbeat.com/connect/token`.
3. Crea el tenant con `POST https://shell.workbeat.com/api/HR/Invitation`,
   mandando el JSON confirmado y el token como `Authorization: Bearer`.
4. Guarda el resultado de la ejecución en dos lugares (el script calcula ambas
   rutas automáticamente, no hace falta indicarlas):
   - Agrega una línea al log acumulado `scripts/tenant_creation_log.jsonl`,
     junto al propio script (historial completo de todas las ejecuciones).
   - Crea un archivo individual dentro de la carpeta `resultado/` en la raíz
     del proyecto, un nivel arriba de `.agent` (por ejemplo
     `<raíz>/resultado/20260731_120000_graco_mexicana.json`), con el JSON de
     entrada y el resultado o error de esa ejecución puntual. Esta carpeta se
     crea automáticamente si no existe — no necesitas crearla tú. (Si el script
     no encuentra `.agent` en ningún nivel superior, usa de respaldo
     `scripts/resultados/` junto a él.)

Si el usuario ya tiene credenciales guardadas (`"credentials_source": "file"`),
el script las toma automáticamente según `scripts/workbeat_config.json` (ver
`scripts/workbeat_config.example.json` para el formato). Si la configuración es
`"prompt"`, ya le pediste usuario/password en el chat y se los pasaste como
`--username`/`--password` (ver punto de control 3) — el script no necesita pedir
nada más.

### Dónde vive el archivo de credenciales

El archivo real de credenciales (`workbeat_credentials.json`) debe colocarse en
`scripts/`, junto al script (nunca compartido ni subido a un repositorio). Usa
`scripts/workbeat_credentials.example.json` como plantilla de formato. Como
contiene un password en texto plano, sugiere al usuario restringir permisos del
archivo o preferir el modo interactivo (`"credentials_source": "prompt"`) si el
entorno es compartido.

## Al instalar esta skill en un equipo nuevo

Como todo vive dentro de la propia carpeta de la skill, instalar el `.skill` ya
deja el script y las plantillas de ejemplo listos — no hay que copiar ni ubicar
ninguna otra carpeta. En ese equipo no existirá todavía
`scripts/workbeat_config.json`, así que la primera vez que se use la skill ahí
se dispara automáticamente la sección "Configuración inicial" de arriba: se le
pregunta al usuario si quiere guardar sus credenciales o que se le pidan cada
vez, y dónde quiere guardar los resultados. No hace falta que nadie edite estos
archivos a mano.

## Después de ejecutar

Reporta al usuario el resultado que devolvió la API (éxito o el error recibido),
y dile en qué archivo de `resultado/` (en la raíz del proyecto) quedó guardado
ese resultado específico (además de que también se agregó al log acumulado
`scripts/tenant_creation_log.jsonl`) para trazabilidad.
