---
name: wbt-doc-test-matrix
description: This skill should be used when the user wants to create test documentation for a Workbeat feature (Phase 4), generate a basic test matrix (casos de prueba), create an extended test matrix covering edge cases, security, performance and accessibility, write acceptance criteria (Definition of Done), create UAT test scenarios, or document test results. Use when the user says things like "crea la matriz de pruebas", "casos de prueba para este feature", "matriz de pruebas extendida", "criterios de aceptación", "definition of done", "pruebas de regresión", "escenarios UAT", "pruebas de seguridad del módulo", "pruebas de rendimiento", "checklist de QA", or "reporte de pruebas".

Do NOT use this skill for creating automated unit tests in code (use test-driven-development skill instead), for requirements documentation (use wbt-doc-requirements), or for release notes (use wbt-doc-release).
version: 1.0.0
---

# wbt-doc-test-matrix — Fase 4: Documentación de Pruebas

Este skill genera los entregables documentales de la Fase 4 del ciclo de vida de documentación de Workbeat.
Consulta `references/test-dimensions.md` para las dimensiones de la matriz extendida y `references/workbeat-dod.md` para el DoD estándar de Workbeat.

## Qué produce este skill

| Entregable | Archivo de salida | Template |
|---|---|---|
| Matriz de pruebas básica | `pruebas/matriz-pruebas.md` | `assets/template-matriz-basica.md` |
| Matriz de pruebas extendida | `pruebas/matriz-pruebas-extendida.md` | `assets/template-matriz-extendida.md` |
| Criterios de aceptación (DoD) | Sección en `06-vision-general.md` | `assets/template-dod.md` |
| Reporte UAT | `pruebas/reporte-uat.md` | `assets/template-reporte-uat.md` |

## Dónde guardar los archivos

```
F:\WBT\Documentacion_Base\features\{nombre-feature}\
└── pruebas\
    ├── matriz-pruebas.md
    ├── matriz-pruebas-extendida.md
    └── reporte-uat.md
```

## Proceso de ejecución

### Paso 1 — Verificar prerequisitos

Para generar la matriz básica, se necesitan:
- `casos-de-uso/` — cada CU genera al menos 2 casos de prueba (happy path + error principal)
- `10-reglas-de-negocio.md` — cada regla critica genera al menos 1 caso de prueba
- `09-precondiciones.md` — las precondiciones generan casos de prueba de validación

Si no existen, preguntar al usuario que describa los flujos principales del feature.

### Paso 2 — Convención de IDs de casos de prueba

Los IDs siguen: `TP-{MODULO}-{NNN}`

| Tipo | ID | Descripción |
|---|---|---|
| Happy path de CU | `TP-{MOD}-001` | Primer caso, siempre el flujo principal exitoso |
| Flujo alternativo | `TP-{MOD}-{N}A` | Sufijo A para alternativas |
| Caso de error | `TP-{MOD}-{N}E` | Sufijo E para errores |
| Edge case | `TP-{MOD}-{N}X` | Sufijo X para extremos |
| Seguridad | `TP-SEC-{NNN}` | Prefijo SEC para seguridad |
| Rendimiento | `TP-PERF-{NNN}` | Prefijo PERF para rendimiento |
| Integración | `TP-INT-{NNN}` | Prefijo INT para integración |

### Paso 3 — Matriz Básica

Generar la matriz básica con cobertura mínima:

**Columnas obligatorias:**
```
| ID | Caso de prueba | Tipo | Actor | Precondición | Pasos | Entrada | Resultado esperado | Resultado real | Estado | CU trazado |
```

**Regla de cobertura mínima:**
- 1 caso happy path por cada caso de uso principal
- 1 caso de error por cada flujo de error documentado
- 1 caso de validación por cada regla de negocio crítica (RN marcadas como `Regulatorio`)
- 1 caso de autorización: acceso con rol correcto + acceso con rol incorrecto

**Estados de caso de prueba:**
- `🔄 Pendiente` — no ejecutado
- `✅ Aprobado` — ejecutado y pasa
- `❌ Fallido` — ejecutado y falla
- `⏭️ Bloqueado` — no se puede ejecutar por dependencia fallida
- `⚠️ Parcial` — pasa con observaciones

### Paso 4 — Matriz Extendida

La matriz extendida cubre 8 dimensiones adicionales. Generar una sección por dimensión:

#### Dimensión 1: Valores límite (Boundary Values)
```
Para cada campo numérico o de fecha:
- Valor = 0 / null / vacío
- Valor = exactamente el límite inferior
- Valor = exactamente el límite superior
- Valor = límite superior + 1 (debe fallar)
```

#### Dimensión 2: Seguridad (siempre incluir en Workbeat)
```
| TP-SEC-001 | JWT expirado | Bearer token con exp en el pasado | 401 Unauthorized |
| TP-SEC-002 | Tenant isolation | Tenant A intenta acceder datos de Tenant B | 403 Forbidden |
| TP-SEC-003 | IDOR | ID de recurso de otro usuario en la URL | 403 o 404 |
| TP-SEC-004 | Missing auth header | Request sin Authorization header | 401 Unauthorized |
| TP-SEC-005 | Cerbos sin permiso | Usuario con JWT válido pero sin política Cerbos | 403 Forbidden |
```

#### Dimensión 3: Autorización por rol
```
Por cada endpoint con [Authorize("Cerbos")]:
- Admin RH puede ejecutar la acción → debe pasar
- Empleado sin permiso intenta ejecutar → 403
- Jefe directo con permiso parcial → según política
```

#### Dimensión 4: Rendimiento
```
| TP-PERF-001 | Tiempo de respuesta P95 | 100 requests concurrentes | < 500ms |
| TP-PERF-002 | Query sin partition key | GET sin tenant en ruta | Alert en logs |
| TP-PERF-003 | Cache miss → DB hit | Invalidar cache y consultar | < 1000ms |
```

#### Dimensión 5: Integración entre microservicios
```
Por cada dependencia con otro módulo Workbeat:
- Módulo origen envía evento a RabbitMQ → módulo destino lo procesa
- CosmosDB partition key correcta en todos los writes
- Redis cache invalidado cuando corresponde
```

#### Dimensión 6: Pruebas de regresión
```
Features existentes que podrían romperse:
- Autenticación JWT (no debe cambiar el flujo)
- Otros endpoints del mismo controller
- Eventos RabbitMQ existentes
```

#### Dimensión 7: Compatibilidad
```
| Plataforma | Versión mínima |
|---|---|
| iOS | 15+ |
| Android | 10+ |
| Chrome | últimas 2 versiones |
| Safari | últimas 2 versiones |
| Edge | últimas 2 versiones |
```

#### Dimensión 8: Accesibilidad (si aplica a UI)
```
- Contraste mínimo WCAG 2.1 AA (4.5:1 para texto normal)
- Navegación por teclado funcional
- Screen reader compatible (atributos aria)
- Touch targets ≥ 44x44px en móvil
```

### Paso 5 — Definition of Done (DoD) estándar Workbeat

Generar el checklist DoD como sección en `06-vision-general.md`:

```markdown
## Criterios de Aceptación (DoD)

### Funcional
- [ ] Todos los casos de prueba de Matriz Básica en estado ✅
- [ ] 0 casos de prueba en estado ❌ sin issue documentado
- [ ] UAT sign-off del Product Manager

### Técnico
- [ ] Cobertura de unit tests ≥ 80% en ApplicationService
- [ ] 0 vulnerabilidades críticas (CVSS ≥ 7.0)
- [ ] Logs estructurados con Serilog para operaciones críticas
- [ ] Trazas en Application Insights para flujos E2E
- [ ] Tenant isolation verificado (TP-SEC-002 aprobado)

### Documentación
- [ ] SemanticDocumentation actualizada (o generada)
- [ ] API Reference completa para todos los endpoints nuevos
- [ ] CLAUDE.md del microservicio actualizado
- [ ] ADRs escritos para decisiones de arquitectura no obvias
- [ ] Matriz de pruebas completa con resultados

### Regulatorio (si aplica)
- [ ] CFDI timbrado correctamente (si módulo NOM)
- [ ] Campos IMSS/SAT validados (si módulo NOM)
- [ ] Datos personales con protección LFPDPPP (siempre)
```

### Paso 6 — Reporte UAT

El reporte UAT se genera después de ejecutar las pruebas con usuarios reales:

```markdown
## Reporte UAT — {Feature} v{X.Y}

**Fecha:** {fecha}
**Participantes:** {lista}
**Entorno:** {staging/producción}
**Versión probada:** {commit o tag}

### Resumen ejecutivo
| Total casos | Aprobados | Fallidos | Bloqueados | % Aprobación |
|---|---|---|---|---|

### Hallazgos
| ID | Severidad | Descripción | Módulo | Estado |
|---|---|---|---|---|
| BUG-001 | 🔴 Crítico | ... | | Abierto |

### Decisión de Go/No-Go
- [ ] ✅ Go — proceder a producción
- [ ] ❌ No-Go — requiere correcciones (lista adjunta)

**Firmado por:** {Product Manager}
```

## Reglas de calidad

- La matriz básica siempre tiene trazabilidad al caso de uso (`CU-{ID}`)
- Los casos de seguridad `TP-SEC-001` a `TP-SEC-005` son obligatorios en TODOS los features de Workbeat
- Los resultados reales nunca se prellenan — se completan durante la ejecución
- La Dimensión 4 (rendimiento) siempre incluye el caso de query sin partition key (antipatrón Workbeat)
- El DoD de documentación siempre requiere CLAUDE.md actualizado
