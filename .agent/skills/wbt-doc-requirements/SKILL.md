---
name: wbt-doc-requirements
description: This skill should be used when the user wants to document requirements for a new Workbeat feature (Phase 1), create use case narratives, define business rules, write the executive summary or vision document, define the feature scope (in/out), create a glossary, document preconditions, build a use case matrix (actors × use cases), or write feature scenarios. Use when the user says things like "documenta los requisitos", "escribe los casos de uso", "define el alcance del feature", "reglas de negocio para este módulo", "glosario de términos", "matriz de casos de uso", "resumen ejecutivo del feature", "precondiciones del sistema", or "visión general de la funcionalidad".

Do NOT use this skill for architecture or technical design documentation (use wbt-doc-design), for test cases (use wbt-doc-test-matrix), or for documenting existing code (use wbt-doc-reverse-engineer).
version: 1.0.0
---

# wbt-doc-requirements — Fase 1: Definición y Análisis

Este skill genera los entregables documentales de la Fase 1 del ciclo de vida de documentación de Workbeat.
Consulta `references/lifecycle.md` para el ciclo completo y `references/business-rules-guide.md` para la convención de IDs de reglas.

## Qué produce este skill

| Entregable | Archivo de salida | Template |
|---|---|---|
| Resumen ejecutivo | `05-resumen-ejecutivo.md` | `assets/template-resumen-ejecutivo.md` |
| Visión general | `06-vision-general.md` | `assets/template-vision-general.md` |
| Contexto y alcance | `07-contexto-y-alcance.md` | `assets/template-contexto-alcance.md` |
| Glosario | `08-glosario.md` | `assets/template-glosario.md` |
| Precondiciones globales | `09-precondiciones.md` | `assets/template-precondiciones.md` |
| Reglas de negocio | `10-reglas-de-negocio.md` | `assets/template-reglas-negocio.md` |
| Casos de uso (narrativas) | `casos-de-uso/CU-{ID}-{nombre}.md` | `assets/template-caso-de-uso.md` |
| Escenarios | `11-escenarios.md` | `assets/template-escenarios.md` |
| Matriz de casos de uso | `12-matriz-casos-de-uso.md` | `assets/template-matriz-cu.md` |

## Dónde guardar los archivos

```
F:\WBT\Documentacion_Base\features\{nombre-feature}\
├── 05-resumen-ejecutivo.md
├── 06-vision-general.md
├── 07-contexto-y-alcance.md
├── 08-glosario.md
├── 09-precondiciones.md
├── 10-reglas-de-negocio.md
├── 11-escenarios.md
├── 12-matriz-casos-de-uso.md
└── casos-de-uso/
    ├── CU-001-{nombre}.md
    └── CU-002-{nombre}.md
```

## Proceso de ejecución

### Paso 1 — Verificar prerequisitos

Verificar que existan los documentos de Fase 0 en `F:\WBT\Documentacion_Base\features\{nombre-feature}\`:
- `04-actores-y-personas.md` — necesario para la matriz de CU y narrativas
- Si no existen, preguntar al usuario si quiere ejecutar **wbt-doc-discovery** primero, o proporcionar la información mínima directamente.

### Paso 2 — Recopilar información de entrada

Preguntar al usuario (o inferir de documentos existentes):

1. **¿Cuáles son los actores del sistema?** (humanos y no-humanos)
2. **¿Cuántos casos de uso principales tiene el feature?** (para nombrarlos CU-001, CU-002...)
3. **¿Existen restricciones regulatorias?** (CFDI, IMSS, SAT, Infonavit — si aplica)
4. **¿Cuál es el módulo de Workbeat afectado?** (ADM, CRH, NOM, ASIST, TALENT, EX)
5. **¿Hay dependencias con otros módulos de Workbeat?** (ej: CRH depende de ADM para empleados)

### Paso 3 — Convención de IDs de reglas de negocio

Los IDs de reglas de negocio siguen el patrón: `RN-{MODULO}-{NNN}`

| Módulo | Prefijo | Ejemplo |
|---|---|---|
| ADM (CoreRH) | `RN-ADM-` | `RN-ADM-001` |
| CRH (Comunicación) | `RN-CRH-` | `RN-CRH-001` |
| NOM (Nómina) | `RN-NOM-` | `RN-NOM-001` |
| ASIST (Asistencia) | `RN-AST-` | `RN-AST-001` |
| TALENT | `RN-TAL-` | `RN-TAL-001` |
| EX (Employee Exp.) | `RN-EX-` | `RN-EX-001` |
| Global / Transversal | `RN-GLB-` | `RN-GLB-001` |

Las reglas globales de Workbeat ya definidas en `references/global-rules.md` se referencian, no se duplican.

### Paso 4 — Convención de IDs de casos de uso

Los IDs de casos de uso siguen: `CU-{MODULO}-{NNN}`

Ejemplo: `CU-AST-001: Solicitar Vacaciones`, `CU-CRH-001: Crear Publicación`

### Paso 5 — Generar documentos

Generar cada documento en el orden de la tabla. Los casos de uso se generan uno por archivo en `casos-de-uso/`. La matriz de casos de uso se genera al final cuando todos los CU están definidos.

### Paso 6 — Criterio de salida de Fase 1

Al finalizar, verificar:
- [ ] Visión general aprobada por stakeholders
- [ ] Alcance con in-scope / out-of-scope explícito
- [ ] Glosario con todos los términos nuevos del dominio
- [ ] Reglas de negocio con ID único y origen (regulatorio / negocio / técnico)
- [ ] Casos de uso con flujo principal + flujos alternativos + flujos de error
- [ ] Matriz de casos de uso completa

Recomendar al usuario continuar con **wbt-doc-design** para la Fase 2.

## Caso de uso: Ingeniería inversa desde Fase 1

Si el feature existe y se necesitan los documentos de Fase 1 retroactivamente:

1. Usar el código fuente del microservicio para inferir los casos de uso (cada endpoint principal = candidato a CU)
2. Inferir las reglas de negocio desde validaciones en el dominio (ApplicationService) y comandos CQRS
3. Construir el glosario desde las entidades del dominio (`Domain/Entities/`)
4. Marcar todos los documentos con `> 📋 Generado por ingeniería inversa`
5. Para el alcance, indicar "este documento describe la funcionalidad ya implementada"

## Reglas de calidad

- El resumen ejecutivo nunca supera 1 página
- Las narrativas de caso de uso siempre incluyen: flujo principal, al menos 1 flujo alternativo, al menos 1 flujo de error
- Las postcondiciones son verificables (no subjetivas)
- Cada regla de negocio referencia su origen: `Regulatorio` / `Negocio` / `Técnico`
- Los casos de uso en la matriz usan: `Inicia` / `Participa` / `Consulta` / `—` (no inventar categorías)
- Todo el glosario incluye el equivalente técnico en código (class/entity name en C#)
