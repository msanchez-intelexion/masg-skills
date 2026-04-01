# Rutas de módulos Workbeat — referencia para skills wbt-doc-*

> Este archivo es leído por los skills `wbt-doc-*` para determinar la ruta de documentación de cada módulo.
> **Fuente de verdad completa:** `F:\WBT\Documentacion_Base\registro-modulos-workbeat.md`

## Mapa rápido módulo → ruta de documentación

| Código | Módulo | Ruta de documentación |
|---|---|---|
| `CRH` | Comunicación RH | `F:\WBT\Microservicios\ComunicacionRH` |
| `ADM` | Core RH / Administración | `F:\WBT\Microservicios\CoreRH` |
| `ONB` | Incorporación / Onboarding | `F:\WBT\Microservicios\Incorporacion_Onboarding` |
| `NOM` | Nómina | `F:\WBT\Microservicios\Nomina` |
| `ASIST` | Asistencia y Vacaciones | `F:\WBT\Microservicios\Asistencia` |
| `TALENT` | Talento | `F:\WBT\Microservicios\Talento` |
| `EX` | Employee Experience | `F:\WBT\Microservicios\EmployeeExperience` |

## Reglas para los skills

1. **Siempre identificar el módulo** antes de crear cualquier archivo de documentación.
2. **Usar la ruta del registro** para guardar todos los archivos generados.
3. Si la funcionalidad no existe en el registro, **preguntar al usuario** antes de crear una nueva carpeta.
4. La documentación transversal siempre va en `{ruta-módulo}\_transversal\`.
5. Si el usuario da una ruta explícita, **usarla tal cual** — la ruta explícita tiene prioridad sobre el registro.
6. Al crear un nuevo archivo, verificar que el directorio existe; si no, crearlo.

## Sub-rutas estándar por funcionalidad

```
{ruta-módulo}\{codigo-funcionalidad}\
├── _assets\                    # Imágenes, mockups, diagramas
├── casos-de-uso\               # CU-{MOD}-{FUN}-NNN.md
├── reglas-de-negocio\          # RN-{MOD}-{FUN}-NNN.md (o RN-{MOD}-{FUN}.md consolidado)
├── matriz-de-pruebas\          # MP-{MOD}-{FUN}.md / MP-EXT-{MOD}-{FUN}.md
├── diagramas\                  # flujo, secuencia, C4
└── ux\                         # wireframes, flujo de pantallas
```

Archivos raíz de cada funcionalidad:
```
{ruta-módulo}\{codigo-funcionalidad}\
├── README.md                   # Índice y alcance de la funcionalidad
├── vision-general.md           # Descripción ejecutiva
└── glosario.md                 # Términos específicos (si no están en _transversal)
```
