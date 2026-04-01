Actúa como **Experto Arquitecto de Software Empresarial**, **Analista de Negocio Senior**, **Experto en Integraciones** y **Especialista en Soluciones Agenticas para diseño de tools (MCP/Tooling AI)** en ecosistemas .NET.

Tu misión es generar un archivo completo llamado `SemanticDocumentation.md` para el sistema Comunicación RH, tomando el código fuente .NET como verdad técnica principal y garantizando cobertura total, precisión semántica y cero omisiones de secciones o endpoints.

## OBJETIVO CRÍTICO
- Producir documentación semántica exhaustiva de APIs y flujos.
- Diseñar la lógica funcional y de integración con enfoque de arquitectura empresarial.
- Incluir reglas de negocio, validaciones, seguridad, dependencias y efectos secundarios por endpoint.
- No omitir ningún endpoint relevante ni ninguna sección obligatoria.
- No inventar información: si un dato no está en código o fuente documental, escribir `No evidenciado en código`.

## IMPORTANTE: ARCHIVOS A OMITIR
- No uses `configurationIndex.md` como fuente (no existirá).
- No asumas índices preconstruidos de cobertura.
- Construye la cobertura directamente desde el código .NET y las fuentes disponibles.

## FUENTES OBLIGATORIAS (ORDEN DE PRECEDENCIA)
1. Código .NET bajo `src/` (fuente de verdad técnica principal).
2. `docs/ComunicacionRH 2.postman_collection.json` (contraste de contratos y ejemplos).
3. `readme.md` y `docs/instructions.md` (contexto operativo).
4. En caso de conflicto, prevalece el código .NET y debes documentar discrepancias.

## ALCANCE OBLIGATORIO DEL ANÁLISIS EN CÓDIGO
Detecta y documenta endpoints en:
- Controllers ASP.NET Core (`[ApiController]`, `[Route]`, `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]`, `[HttpPatch]`)
- Minimal APIs (`MapGet`, `MapPost`, `MapPut`, `MapDelete`, `MapPatch`)
- Rutas versionadas (`/api/v1/...`)

Extrae para cada endpoint:
- Método HTTP y ruta completa
- Parámetros de Path, Query, Body y Header
- DTOs request/response y tipos
- Validaciones (DataAnnotations, FluentValidation, validaciones de dominio)
- Seguridad (`[Authorize]`, policies, roles, claims, Cerbos, Workbeat Action si aplica)
- Reglas de negocio en servicios/aplicación/dominio
- Dependencias cruzadas (repositorios, tablas, colas/eventos, integraciones)
- Efectos secundarios (persistencia, bitácora, publicaciones de eventos, recalculos)
- Códigos HTTP y manejo de errores reales
- Variantes de exportación (`/Exportar`) y paginación/filtros

## ENFOQUE AGÉNTICO Y DISEÑO DE TOOLS (OBLIGATORIO)
Además de documentar endpoints, debes analizar cómo se traducen a tools para agentes de IA:
- Identifica intención de negocio por endpoint.
- Propón agrupación por dominio funcional (no por verbo HTTP).
- Define cuándo usar cada tool y cuándo NO usarla.
- Define dependencias entre tools y secuencias determinísticas.
- Señala precondiciones de seguridad/contexto (`tenant`, token, rol) para cada tool.
- Marca operaciones de lectura vs escritura y riesgos operativos.
- Incluye recomendaciones de guard rails para evitar ejecuciones incorrectas.

## ESTRUCTURA OBLIGATORIA DEL ARCHIVO RESULTANTE
Genera SOLO markdown final de `SemanticDocumentation.md`, sin texto adicional fuera del documento.

Debe incluir exactamente:

1. `## 1. Introducción`
2. `## 2. Glosario de Conceptos`
3. `## 3. Información General de Seguridad`
4. `## 4. Información General sobre Búsquedas y Paginación`
5. `## 5. Códigos de Respuesta y Errores`
6. Secciones por endpoint (numeradas y agrupadas por dominio funcional detectado desde código)
7. `## Anexo A — Matriz de Cobertura`
8. `## Anexo B — Inconsistencias Detectadas`
9. `## Anexo C — Checklist de Completitud`
10. `## Anexo D — Diseño de Tools para Agente IA (MCP)`

## PLANTILLA OBLIGATORIA POR ENDPOINT
Para CADA endpoint, usa este formato exacto y en este orden:

## [ID autogenerado] [Nombre funcional]
**Endpoint:** `[VERBO] [ruta]`  
**Type:** `[Configuración Esencial 🟢 | Configuración Completa 🔵 | Configuración Avanzada 🟣]`

### Descripción semántica
### Precondiciones
### Parámetros
Tabla con columnas:
`Parámetro | Tipo | Requerido | Default | Fuente | Descripción`
### Body
- JSON de ejemplo válido si aplica
- Si no aplica: `No aplica`
### Respuesta exitosa
### Códigos de respuesta
Tabla con columnas:
`Código | Descripción`
### Reglas de negocio
### Efectos secundarios
### Dependencias cruzadas
### Notas para agente de IA

Regla estricta: ninguna subsección puede omitirse; si no aplica, escribir `No aplica`.

## MATRIZ DE COBERTURA SIN ÍNDICE PREVIO (OBLIGATORIO)
Como no existe `configurationIndex.md`, construye una cobertura propia:
- Lista maestra de endpoints detectados en código.
- Marca cuáles están en Postman.
- Marca cuáles aparecen en documentación previa (si existe).
- Marca cuáles son solo código (no documentados antes).
- Marca cuáles son solo Postman (no encontrados en código).

## ANEXO A — MATRIZ DE COBERTURA (FORMATO)
Tabla:
`Endpoint código | Método | En Postman | En docs previas | Estado de documentación | Fuente principal`

Estados sugeridos:
- `Documentado`
- `Detectado en código (nuevo)`
- `Solo en Postman`
- `Solo en documentación previa`
- `No evidenciado en código`

## ANEXO B — INCONSISTENCIAS DETECTADAS
Lista de discrepancias entre:
- código .NET
- documentación previa
- Postman collection

Para cada inconsistencia:
- Qué difiere
- Evidencia
- Impacto
- Recomendación

## ANEXO C — CHECKLIST DE COMPLETITUD
Checklist mínimo:
- Todos los endpoints detectados en código están documentados
- Todas las secciones por endpoint están presentes
- No hay secciones vacías sin `No aplica`
- No hay datos inventados
- Seguridad global documentada
- Paginación/filtros documentados
- Exportaciones documentadas
- Discrepancias registradas
- Trazabilidad completa