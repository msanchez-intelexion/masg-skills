# Contexto de Negocio — Workbeat HCM

## ¿Qué es Workbeat?

Workbeat es una plataforma SaaS de Gestión de Capital Humano (HCM) multi-tenant orientada al mercado mexicano. Resuelve la fragmentación de sistemas RH integrando seis áreas funcionales en una sola plataforma.

## Los 6 Módulos Funcionales

### 1. Administración de Colaboradores (ADM / CoreRH)
- Altas, bajas y movimientos (onboarding/offboarding)
- Expediente digital del empleado
- Estructura organizacional
- Gestión de posiciones y puestos
- Integración con SAT, IMSS, Infonavit (catálogos)

### 2. Nómina y Cumplimiento (NOM)
- Cálculo de nómina
- Timbrado CFDI (SAT)
- Integración IMSS, SAT, Infonavit (obligaciones patronales)
- Incidencias y variables de nómina

### 3. Asistencia y Vacaciones (ASIST)
- Control de asistencia
- Reconocimiento facial / geolocalización
- Solicitudes y aprobaciones de vacaciones
- Saldos de días

### 4. Atracción y Desarrollo de Talento (TALENT)
- Reclutamiento y selección
- Evaluaciones de desempeño
- Capacitación y cursos
- Gestión del desempeño

### 5. Comunicación Organizacional (CRH)
- Publicaciones y noticias internas
- Campañas de comunicación
- Eventos corporativos
- Apps de contenido (Cultura, TV corporativa, espacios digitales)
- Notificaciones multicanal (push, email, SMS)

### 6. Employee Experience / Experiencia del Empleado (EX)
- Superapp móvil del colaborador
- Autoservicio (solicitudes, documentos, recibos)
- Servicios al empleado
- Contenido personalizado

## Actores Estándar del Sistema

| Actor | Descripción | Módulos principales |
|---|---|---|
| **Empleado** | Usuario final, colaborador activo | Todos (vista limitada) |
| **Jefe directo** | Aprueba solicitudes de su equipo | ASIST, TALENT |
| **Administrador RH** | Configura, reporta, gestiona | ADM, NOM, CRH, ASIST |
| **Superadministrador** | Configura el tenant completo | Todos |
| **Integrador técnico** | Conecta sistemas externos via API | API de todos los módulos |
| **Agente de IA** | Asiste via MCP tools | MCP servers de CRH, ADM |
| **Sistema externo** | SAT, IMSS, Infonavit, sistemas legacy | NOM, ADM |

## Stack Tecnológico (resumen para documentación)

- **Backend:** C# / .NET 8, ASP.NET Core Web API
- **Base de datos:** Azure CosmosDB (NoSQL, partition key por tenant+año)
- **Mensajería:** RabbitMQ (eventos asíncronos, DLQ con 5 reintentos)
- **Caché:** Redis (L2) + MemoryCache (L1)
- **Auth:** JWT (IdentityServer4) + Cerbos (políticas de autorización)
- **Functions:** Azure Functions (Isolated Worker, .NET 8)
- **IA:** OpenAI, Leonardo AI, MCP tools
- **Storage:** Azure Blob Storage, Azure CDN
- **Observabilidad:** Serilog + Application Insights

## Convenciones críticas de Workbeat

| Convención | Descripción |
|---|---|
| `id` en minúsculas | CosmosDB es case-sensitive; todos los IDs en lowercase |
| Partition key | `{Año}-{TenantId}` — toda query debe incluirlo |
| Soft delete | Nunca se elimina físicamente; usar `DeletedBy` |
| Auditoría automática | `CreatedBy/UpdatedBy/DeletedBy` desde claims JWT |
| Tenant isolation | Cada organización tiene datos completamente aislados |
| URL base | `api/v1/{tenant:guid}/{módulo}/[controller]` |
| Caché L1→L2→DB | Invalidar ambos niveles al modificar datos |
| DLQ | 5 reintentos en RabbitMQ → Dead-Letter Queue |
