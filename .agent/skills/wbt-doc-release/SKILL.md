---
name: wbt-doc-release
description: This skill should be used when the user wants to create release documentation for a Workbeat feature (Phases 5, 6, 7), write release notes, create a rollout plan, track time to market (TTM), generate stakeholder communication, create training materials for different audiences (employees, HR admins, tech integrators), write getting-started guides or how-to guides, generate operational runbooks, create troubleshooting guides, or document post-incident reports. Use when the user says things like "escribe las release notes", "plan de rollout", "tracker de time to market", "material de capacitación", "guía para el administrador de RH", "getting started del feature", "runbook operacional", "guía de troubleshooting", "comunicado del lanzamiento", "how-to guide", "capacitación para empleados", or "post-mortem del incidente".

Do NOT use this skill for test matrices (use wbt-doc-test-matrix), for requirements (use wbt-doc-requirements), or for creating code documentation (use wbt-doc-reverse-engineer).
version: 1.0.0
---

# wbt-doc-release — Fases 5-7: Release, Capacitación y Soporte

Este skill genera los entregables documentales de las Fases 5, 6 y 7 del ciclo de vida de documentación de Workbeat.
Consulta `references/audience-guide.md` para el tono y nivel técnico adecuado por audiencia.

## Qué produce este skill

### Fase 5 — Release
| Entregable | Archivo de salida | Template |
|---|---|---|
| Release notes | `releases/v{X.Y.Z}.md` | `assets/template-release-notes.md` |
| Plan de rollout | `releases/rollout-plan.md` | `assets/template-rollout.md` |
| TTM Tracker | `releases/ttm-tracker.md` | `assets/template-ttm.md` |
| Comunicado stakeholders | `releases/comunicado-v{X.Y.Z}.md` | `assets/template-comunicado.md` |

### Fase 6 — Capacitación
| Entregable | Archivo de salida | Audiencia |
|---|---|---|
| Tutorial getting started | `guides/getting-started.md` | Todos |
| Guías how-to por caso de uso | `guides/{verbo}-{objeto}.md` | Según actor |
| Material empleado final | `capacitacion/empleado.md` | Empleado |
| Material jefe directo | `capacitacion/jefe.md` | Jefe directo |
| Material administrador RH | `capacitacion/admin-rh.md` | Admin RH |
| Material integrador técnico | `capacitacion/integrador.md` | Integrador |
| Actualización CLAUDE.md | `CLAUDE.md` del microservicio | Agente IA |

### Fase 7 — Soporte
| Entregable | Archivo de salida | Template |
|---|---|---|
| Runbook operacional | `soporte/runbook.md` | `assets/template-runbook.md` |
| Guía de troubleshooting | `soporte/troubleshooting.md` | `assets/template-troubleshooting.md` |
| Registro de incidencia | `soporte/incidencias/INC-{N}-{titulo}.md` | `assets/template-incidencia.md` |

## Dónde guardar los archivos

```
F:\WBT\Documentacion_Base\features\{nombre-feature}\
├── releases\
│   ├── v{X.Y.Z}.md
│   ├── rollout-plan.md
│   ├── ttm-tracker.md
│   └── comunicado-v{X.Y.Z}.md
├── guides\
│   ├── getting-started.md
│   └── {verbo}-{objeto}.md
├── capacitacion\
│   ├── empleado.md
│   ├── jefe.md
│   ├── admin-rh.md
│   └── integrador.md
└── soporte\
    ├── runbook.md
    ├── troubleshooting.md
    └── incidencias\
        └── INC-{N}-{titulo}.md
```

## Proceso de ejecución

### Fase 5 — Release

#### Paso 1 — Release Notes

Versionar el feature con SemVer: `MAJOR.MINOR.PATCH`
- MAJOR: cambios que rompen compatibilidad (breaking changes)
- MINOR: nuevas funcionalidades retrocompatibles
- PATCH: correcciones de bugs

**Estructura obligatoria:**
```markdown
# Release Notes — v{X.Y.Z}
**Fecha:** {YYYY-MM-DD}  
**Módulo:** {CRH | ADM | NOM | ASIST | TALENT | EX}  
**Tipo:** {Feature | Bugfix | Hotfix | Breaking Change}

## ✨ Nuevas funcionalidades
- [descripción en lenguaje de negocio, no técnico]

## 🔧 Mejoras
- [qué mejoró y cómo afecta al usuario]

## 🐛 Bugs corregidos
- [descripción del bug y fix]

## ⚠️ Breaking Changes
- [qué cambia, cómo migrar]

## 📋 Instrucciones de actualización
- [pasos si hay configuración o migración requerida]
```

#### Paso 2 — Plan de Rollout

```markdown
# Plan de Rollout — v{X.Y.Z}

## Estrategia de despliegue
- [ ] Fase 1: Canary (1-2 tenants piloto) — verificar por 24h
- [ ] Fase 2: 10% de tenants — verificar por 48h
- [ ] Fase 3: 50% de tenants — verificar por 48h
- [ ] Fase 4: 100% de tenants

## Feature Flags
| Flag | Estado inicial | Quién activa |
|---|---|---|
| `{feature-flag-name}` | OFF | DevOps |

## Criterios de rollback
- Error rate > 1% en las primeras 2 horas → rollback automático
- Cualquier P0 reportado en primeras 4 horas → rollback manual

## Tenants piloto
| Tenant | Nombre | Contacto |
|---|---|---|
```

#### Paso 3 — TTM Tracker

Calcular tiempo real vs. estimado por fase:

```markdown
# TTM Tracker — {Feature}

| Fase | Inicio | Fin | Días reales | Días estimados | Delta |
|---|---|---|---|---|---|
| F0 Descubrimiento | | | | | |
| F1 Definición | | | | | |
| F2 Diseño | | | | | |
| F3 Construcción | | | | | |
| F4 Pruebas | | | | | |
| F5 Release | | | | | |
| **TOTAL** | | | | | |

## Lecciones aprendidas
- **Qué salió bien:**
- **Cuellos de botella:**
- **Mejoras para el próximo ciclo:**
```

### Fase 6 — Capacitación

#### Nivel técnico por audiencia

| Audiencia | Tono | Tecnicidad | Longitud |
|---|---|---|---|
| **Empleado final** | Informal, amigable | Sin términos técnicos | Muy corto (< 500 palabras) |
| **Jefe directo** | Semi-formal | Términos de negocio, sin código | Corto (< 800 palabras) |
| **Administrador RH** | Formal, instructivo | Términos de configuración | Medio (< 1500 palabras) |
| **Integrador técnico** | Técnico, preciso | Endpoints, JSON, código | Largo (sin límite) |
| **Soporte L1** | Técnico, orientado a acción | Síntomas y soluciones | Medio (< 1000 palabras) |
| **Agente de IA** | Estructurado, exhaustivo | Técnico completo | Sin límite |

#### Getting Started — estructura obligatoria

```markdown
# Primeros pasos con {Feature}

**¿Qué puedes hacer ahora?** {1 oración de valor}

## Antes de empezar
- Prerequisito 1
- Prerequisito 2

## Paso 1 — {acción concreta}
{captura de pantalla o descripción visual}

## Paso 2 — {acción concreta}
...

## ¡Listo! Qué sigue
- [{siguiente acción recomendada}]({link})
```

#### How-to Guides — estructura obligatoria

```markdown
# Cómo {verbo} {objeto}

**Audiencia:** {actor}  
**Tiempo estimado:** {N minutos}  
**Prerequisitos:** {lista}

## Pasos
1. {paso concreto con verbo imperativo}
2. ...

## Resultado esperado
{qué ve el usuario cuando el proceso es exitoso}

## Si algo falla
- Síntoma X → solución Y
- Ver [Guía de troubleshooting]({link})
```

#### Actualización de CLAUDE.md (Agente IA)

Si el feature agrega capacidades nuevas al microservicio:
1. Leer el `CLAUDE.md` actual del microservicio en `C:\Microservicios\{nombre}\`
2. Agregar el feature a la sección de capacidades o endpoints
3. Agregar gotchas o convenciones nuevas si las hay
4. Actualizar el conteo de endpoints si aplica

### Fase 7 — Soporte

#### Runbook — estructura obligatoria

```markdown
# Runbook — {Feature}
**Versión:** {X.Y.Z}  
**Equipo responsable:** {team}  
**Escalada a:** {contacto o equipo senior}

## Verificación de salud
```powershell
# Health check
GET https://{env}.workbeat.com/api/v1/values
```

## Síntomas comunes y diagnóstico

### Síntoma: {descripción del problema}
**Causa probable:** {causa}
**Diagnóstico:**
1. Verificar logs en Application Insights: `{query KQL}`
2. Revisar DLQ en RabbitMQ: `{nombre de la queue}`
3. Verificar estado de Redis: `{comando}`

**Resolución:**
1. {paso de resolución}

**Cuándo escalar:** {criterio}

## Comandos útiles
```powershell
# Ver logs en tiempo real
# Limpiar cache de Redis
# Re-procesar mensajes de DLQ
```
```

#### Troubleshooting — estructura obligatoria

```markdown
# Guía de Troubleshooting — {Feature}

## Errores HTTP frecuentes

| Código | Mensaje | Causa | Solución |
|---|---|---|---|
| 401 | Unauthorized | JWT expirado o inválido | Renovar token |
| 403 | Forbidden | Sin permisos Cerbos | Verificar rol del usuario |
| 404 | Not Found | Recurso no existe o tenant incorrecto | Verificar tenant GUID |
| 422 | Unprocessable Entity | Validación de negocio fallida | Ver detalle en `errors` |
| 500 | Internal Server Error | Error no manejado | Ver logs Application Insights |

## Problemas de configuración frecuentes
## Preguntas frecuentes (FAQ)
```

## Reglas de calidad

- El material de capacitación para empleados nunca menciona términos como JWT, tenant, partition key
- Los release notes describen el impacto al usuario, no los cambios técnicos internos
- Los runbooks incluyen queries KQL reales de Application Insights cuando existen
- El TTM Tracker se completa con fechas reales, nunca con estimaciones retroactivas
- Las guías How-to comienzan con verbo imperativo: "Solicitar", "Configurar", "Exportar"
- El CLAUDE.md se actualiza en cada release que agrega endpoints o cambia comportamientos
