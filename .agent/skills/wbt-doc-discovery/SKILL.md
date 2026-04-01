---
name: wbt-doc-discovery
description: This skill should be used when the user wants to start documenting a new Workbeat feature or module from scratch (Phase 0), generate discovery documentation, create brainstorming records, document design thinking sessions, define Jobs to Be Done (JTBD) for a feature, create metapersonas or actor definitions, or write a project kick-off document for a Workbeat product initiative. Use when the user says things like "quiero documentar una nueva funcionalidad", "vamos a iniciar la fase de descubrimiento", "crea el brainstorming de este feature", "define los actores para este módulo", "JTBD para esta funcionalidad", or "kick-off de documentación".

Do NOT use this skill for general brainstorming unrelated to Workbeat documentation (use the superpowers brainstorming skill instead), for creating agents or plugins (use agent-development), or for documenting existing code (use wbt-doc-reverse-engineer).
version: 1.0.0
---

# wbt-doc-discovery — Fase 0: Descubrimiento e Ideación

Este skill genera los entregables documentales de la Fase 0 del ciclo de vida de documentación de Workbeat.
Consulta `references/lifecycle.md` para el contexto completo del ciclo y `references/workbeat-context.md` para el dominio de negocio.

## Qué produce este skill

| Entregable | Archivo de salida | Template |
|---|---|---|
| Acta de kick-off | `00-kickoff.md` | `assets/template-kickoff.md` |
| Registro de brainstorming | `01-brainstorming.md` | `assets/template-brainstorming.md` |
| Canvas de Design Thinking | `02-design-thinking.md` | `assets/template-design-thinking.md` |
| Jobs to Be Done | `03-jtbd.md` | `assets/template-jtbd.md` |
| Metapersonas y Actores | `04-actores-y-personas.md` | `assets/template-actores.md` |

## Dónde guardar los archivos

**Consultar SIEMPRE `references/module-paths.md`** para obtener la ruta correcta según el módulo.

| Módulo | Ruta base de documentación |
|---|---|
| CRH — Comunicación RH | `F:\WBT\Microservicios\ComunicacionRH` |
| ADM — Core RH | `F:\WBT\Microservicios\CoreRH` |
| ONB — Incorporación | `F:\WBT\Microservicios\Incorporacion_Onboarding` |

Los entregables de discovery van en la carpeta de la funcionalidad correspondiente:

```
{ruta-módulo}\{nombre-funcionalidad}\
├── 00-kickoff.md
├── 01-brainstorming.md
├── 02-design-thinking.md
├── 03-jtbd.md
└── 04-actores-y-personas.md
```

Si la carpeta de la funcionalidad no existe, ejecutar el script de scaffold:
```powershell
.\scripts\scaffold_module.ps1 -Module CRH   # o ADM / ONB
```

El nombre de funcionalidad debe coincidir con los definidos en `references/module-paths.md`.

## Proceso de ejecución

### Paso 1 — Recopilar contexto

Antes de generar cualquier documento, preguntar al usuario:

1. **¿Cuál es el nombre del feature o módulo?** (para nombrar la carpeta)
2. **¿A qué módulo de Workbeat pertenece?** (ADM, CRH, NOM, ASIST, TALENT, EX)
3. **¿Qué problema de negocio resuelve?** (1-3 oraciones)
4. **¿Qué documentos de Fase 0 se necesitan?** (todos, o selección específica)
5. **¿Ya se realizó alguna sesión de discovery?** (para incluir hallazgos reales)

Si el usuario proporciona notas, transcripciones de sesiones o descripciones del problema, incorporarlas en los documentos.

### Paso 2 — Crear carpeta del feature

```powershell
New-Item -ItemType Directory -Force -Path "F:\WBT\Documentacion_Base\features\{nombre-feature}"
```

### Paso 3 — Generar documentos

Generar cada documento usando el template correspondiente en `assets/`. Adaptar el contenido al feature específico; no dejar placeholders vacíos. Si falta información, usar contenido inferido del contexto y marcarlo con `> ⚠️ Pendiente de validar con el equipo`.

### Paso 4 — Criterio de salida de Fase 0

Al finalizar, verificar:
- [ ] Problema de negocio articulado con POV Statement
- [ ] Al menos 3 actores/metapersonas definidos
- [ ] JTBD documentados para cada actor principal
- [ ] Acta de kick-off firmada (indica Go/No-Go)

Recomendar al usuario continuar con **wbt-doc-requirements** para la Fase 1.

## Caso de uso: Ingeniería inversa desde Fase 0

Si el feature ya existe pero falta documentación de discovery:

1. Revisar el código en `C:\Microservicios\` para inferir el propósito y actores
2. Inferir JTBD desde los endpoints y entidades del dominio
3. Marcar todos los documentos con `> 📋 Generado por ingeniería inversa — validar con el equipo de producto`
4. Sugerir al usuario complementar con entrevistas o revisión de stakeholders

## Reglas de calidad

- El POV Statement siempre sigue la estructura: `[Metapersona] necesita [necesidad] porque [insight]`
- Los Job Statements siempre siguen: `Cuando [situación], quiero [motivación], para [resultado]`
- Los Outcome Statements son medibles: usar verbos como "minimizar", "maximizar", "reducir"
- Los actores de Workbeat siempre incluyen al **Agente de IA** como actor no-humano
- Nunca omitir el módulo de Workbeat al que pertenece el feature
