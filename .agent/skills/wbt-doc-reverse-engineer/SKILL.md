---
name: wbt-doc-reverse-engineer
description: This skill should be used when the user wants to generate documentation from existing Workbeat source code (reverse engineering / ingeniería inversa), document a module that was already implemented but has no documentation, generate SemanticDocumentation from C# code, extract API reference from controllers, document the domain model from entities and commands, create Architecture Decision Records (ADRs) from existing patterns, or produce a progressive configuration index from existing endpoints. Use when the user says things like "genera la documentación del código existente", "ingeniería inversa del microservicio", "documenta este controller", "semantic documentation desde el código", "extrae los endpoints de este controller", "documenta el dominio de CRH", "ADRs del código existente", or "el feature ya está implementado, necesito documentarlo".

Do NOT use this skill for documenting new features not yet built (use wbt-doc-discovery → wbt-doc-requirements → wbt-doc-design instead), for test matrices (use wbt-doc-test-matrix), or for release documentation (use wbt-doc-release).
version: 1.0.0
---

# wbt-doc-reverse-engineer — Ingeniería Inversa: Código → Documentación

Este skill analiza código fuente C# de Workbeat y genera documentación completa. Es el camino rápido para documentar funcionalidades ya implementadas.
Consulta `references/csharp-patterns.md` para los patrones arquitectónicos de Workbeat y `references/cosmos-conventions.md` para las convenciones de CosmosDB.

## Qué produce este skill

| Entregable | Archivo de salida | Fuente de análisis |
|---|---|---|
| Documentación semántica | `{Modulo}_SemanticDocumentation.md` | Dominio + API completa |
| Referencia de API por controller | `api/{Controller}.md` | Archivos `*Controller.cs` |
| Documentación del dominio | `dominio/entidades.md` | `Domain/Entities/*.cs` |
| Enums del dominio | `dominio/enums.md` | `Domain/Enums/*.cs` |
| ADRs inferidos | `decisiones/ADR-{N}-{titulo}.md` | Patrones en código |
| Índice de configuración progresiva | `IndiceMaestroConfiguracion.md` | Todos los endpoints |
| Principios y gotchas | `principles.md` | Patrones cross-cutting |

## Dónde guardar los archivos

### Para módulo existente (documentación de código):
```
F:\WBT\Documentacion_Base\{modulo}\
├── {Modulo}_SemanticDocumentation.md
├── IndiceMaestroConfiguracion.md
├── arquitectura.md
├── principles.md
├── api/
│   ├── README.md
│   └── {Controller}.md
└── dominio/
    ├── README.md
    ├── entidades.md
    └── enums.md
```

### Para feature específico (complementar docs existentes):
```
F:\WBT\Documentacion_Base\features\{nombre-feature}\
├── SemanticDocumentation.md
├── api\{Controller}.md
├── dominio\entidades.md
└── decisiones\ADR-{N}-{titulo}.md
```

## Proceso de ejecución

### Paso 1 — Identificar el microservicio o feature

Preguntar al usuario:
1. **¿Qué microservicio o feature se va a documentar?** (CRH, CoreRH, NOM, ASIST, TALENT, EX, o feature específico)
2. **¿Cuál es la ruta al código fuente?** (por defecto: `C:\Microservicios\{nombre}\src\`)
3. **¿Qué documentos se necesitan?** (todos, o selección específica)

### Paso 2 — Análisis del código fuente

Ejecutar `scripts/analyze-csharp.py` para extraer información estructurada:

```powershell
python F:\WBT\.agent\skills\wbt-doc-reverse-engineer\scripts\analyze-csharp.py `
  --src "C:\Microservicios\{nombre}\src" `
  --output "F:\WBT\Documentacion_Base\{modulo}" `
  --mode summary
```

Si el script no está disponible, analizar manualmente:

**Para Controllers (→ API Reference):**
- Buscar archivos `*Controller.cs` en `src\*Api\Controllers\`
- Por cada controller: extraer route base (`[Route]`), método HTTP, nombre del action, parámetros, `[Authorize]` o `[AllowAnonymous]`
- Usar `grep` para buscar patrones: `\[HttpGet\]`, `\[HttpPost\]`, `\[HttpPut\]`, `\[HttpDelete\]`, `\[Route\(`

**Para Entidades del Dominio (→ dominio/entidades.md):**
- Buscar archivos en `src\*Domain\Entities\` y `src\*Domain\`
- Extraer: nombre de clase, propiedades con tipos, métodos públicos, clase base heredada
- Identificar: invariantes (validaciones en constructor), value objects usados

**Para Enums (→ dominio/enums.md):**
- Buscar archivos `*enum*.cs` o carpeta `Enums/`
- Extraer: nombre del enum, valores, descripción de negocio (inferir si no hay XML docs)

**Para Commands CQRS (→ dominio/entidades.md):**
- Buscar `record` types con sufijo `Command` o en carpeta `Commands/`
- Extraer: campos del record, handler asociado

### Paso 3 — Generar SemanticDocumentation

La SemanticDocumentation es el documento central. Estructura obligatoria:

```markdown
# Documentación Semántica — Sistema {NOMBRE} ({Descripción})
> Versión: X.0 — Generada por ingeniería inversa desde código fuente
> Audiencia: Usuarios no técnicos, administradores, integradores, agentes de IA

## 1. Introducción
## 2. Glosario de Conceptos
## 3. Capacidades por Módulo / Controller
## 4. Flujos de Proceso Principales
## 5. Modelos de Datos Clave
## 6. Reglas de Negocio Identificadas
## 7. Convenciones Técnicas Importantes (Gotchas)
```

Traducir nombres técnicos a lenguaje de negocio:
- `PublicacionController` → "Gestión de Publicaciones Internas"
- `Tenant` (partition key) → "Identificador único de la organización"
- `soft delete` (`DeletedBy`) → "Las publicaciones nunca se eliminan físicamente"

### Paso 4 — Generar API Reference por Controller

Para cada controller, generar `api/{Controller}.md` con la estructura:

```markdown
# {Controller} — {descripción de negocio}
URL base: `api/v1/{tenant:guid}/{módulo}/{recurso}`
Autenticación: [Público | JWT | Cerbos]

## Endpoints
| # | Método | Ruta | Descripción | Auth |
|---|---|---|---|---|

## Detalle de Endpoints
### {METHOD} {ruta} — {Nombre del endpoint}
**Descripción:** {qué hace en lenguaje de negocio}
**Autenticación:** {tipo}
**Parámetros:** {tabla}
**Request body:** {JSON example si aplica}
**Respuestas:** {tabla con código HTTP, descripción, ejemplo}
```

### Paso 5 — Inferir ADRs desde patrones

Buscar patrones recurrentes en el código que representen decisiones de arquitectura:

| Patrón encontrado | ADR a documentar |
|---|---|
| Partition key `{Año}-{TenantId}` | ADR: Partition key compuesta para CosmosDB |
| `id` siempre en minúsculas | ADR: Normalización de IDs en CosmosDB |
| Clase base `Catalogo` | ADR: Modelo de dominio con clase base unificada |
| MemoryCache → Redis → CosmosDB | ADR: Caché de dos niveles |
| Retry 5 veces → DLQ | ADR: Política de reintentos en RabbitMQ |
| `record` types para commands | ADR: Inmutabilidad en commands CQRS |
| `[Authorize("Cerbos")]` | ADR: Autorización por políticas con Cerbos |

### Paso 6 — Generar Índice Maestro de Configuración

El `IndiceMaestroConfiguracion.md` organiza todos los endpoints en fases ordenadas por dependencias:

**Plantilla de fase:**
```markdown
## Fase {N} — {Nombre de Fase}
**Objetivo:** {qué se logra}
**Dependencias:** {fases previas requeridas}

| # | Método | Ruta | Descripción | Dependencias |
|---|---|---|---|---|
```

**Orden de fases estándar de Workbeat:**
- Fase 0: Health check y recursos públicos (sin auth)
- Fase 1: Inicialización del módulo (JWT básico)
- Fase 2+: Configuración de catálogos (dependencias simples)
- Fases finales: Entidades principales y procesos

### Paso 7 — Marcar el tipo de documento

Todo documento generado por ingeniería inversa incluye en el header:
```
> 📋 **Generado por ingeniería inversa** desde código fuente  
> Versión de código analizada: {fecha o commit}  
> ⚠️ Validar con el equipo de producto que refleja el comportamiento actual
```

## Integración con el ciclo de vida completo

Si el usuario quiere documentación completa (todas las fases) desde código existente:

1. **wbt-doc-reverse-engineer** genera: SemanticDoc, API Reference, Domain docs, ADRs (Fases 3, parte de 1 y 2)
2. **wbt-doc-discovery** completa: JTBD, actores, brainstorming retroactivo (Fase 0)
3. **wbt-doc-requirements** completa: Casos de uso, reglas de negocio, glosario (Fase 1)
4. **wbt-doc-design** completa: Arquitectura C4, diagramas de secuencia (Fase 2)
5. **wbt-doc-test-matrix** genera: Matrices de prueba (Fase 4)
6. **wbt-doc-release** genera: Docs de soporte y capacitación (Fases 6-7)

## Reglas de calidad

- La SemanticDocumentation siempre está en lenguaje de negocio (no técnico)
- Los endpoints se cuentan y se documenta el total en el header del documento
- Los IDs de endpoints siguen el patrón: `{SIG-NNN}` donde SIG = siglas del controller (PUB = Publicacion, NOT = Notificacion, etc.)
- Los gotchas y convenciones técnicas se extraen de patrones repetidos en el código
- Las reglas de negocio inferidas se marcan como `🔍 Inferido — validar`
- Nunca inventar comportamientos que no estén en el código
