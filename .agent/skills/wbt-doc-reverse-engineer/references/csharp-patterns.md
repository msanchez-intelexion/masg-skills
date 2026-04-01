# Patrones de Análisis C# — Workbeat

## Cómo localizar archivos relevantes

### Controllers (→ API Reference)
```powershell
Get-ChildItem "C:\Microservicios\{nombre}\src" -Recurse -Filter "*Controller.cs"
```

Extraer de cada controller:
- `[Route("api/v1/...")]` → URL base
- `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]` → método HTTP
- `[Authorize]`, `[AllowAnonymous]`, `[Authorize("Cerbos")]` → tipo de auth
- Nombre del método → nombre del endpoint
- Parámetros `([FromQuery]`, `[FromBody]`, `[FromRoute]`) → parámetros del endpoint

### Entidades del Dominio (→ dominio/entidades.md)
```powershell
Get-ChildItem "C:\Microservicios\{nombre}\src\*Domain*" -Recurse -Filter "*.cs" |
  Where-Object { $_.Name -notmatch "(Command|Enum|ValueObject|Exception)" }
```

Extraer de cada entidad:
- Propiedades públicas con sus tipos
- Clase base heredada (normalmente `Catalogo`)
- Métodos públicos (especialmente `Crear`, `Modificar`, `Eliminar`, `Contextualizar`)
- Invariantes en el constructor o en métodos de creación

### Commands CQRS (→ dominio/entidades.md, sección Commands)
```powershell
Get-ChildItem "C:\Microservicios\{nombre}\src\*Domain*" -Recurse -Filter "*Command*.cs"
# También buscar records con sufijo Command
Select-String -Path "**\*.cs" -Pattern "^public record.*Command"
```

### Enums (→ dominio/enums.md)
```powershell
Get-ChildItem "C:\Microservicios\{nombre}\src\*Domain*" -Recurse -Filter "*Enum*.cs"
Get-ChildItem "C:\Microservicios\{nombre}\src\*Domain*\Enums" -Recurse
```

### Value Objects
```powershell
Get-ChildItem "C:\Microservicios\{nombre}\src\*Domain*\ValueObjects" -Recurse
```

## Patrones de arquitectura Workbeat a identificar

### Patrón: Clase base Catalogo
```csharp
// Todas las entidades principales heredan de Catalogo
public class Publicacion : Catalogo { ... }
// → ADR: Modelo de dominio con clase base unificada
```

### Patrón: Partition Key compuesta
```csharp
// CosmosDB partition key: {Año}-{TenantId}
[PartitionKey]
public string PartitionKey => $"{FechaCreacion.Year}-{Tenant}";
// → ADR: Partition key compuesta para distribución eficiente
```

### Patrón: Soft Delete
```csharp
public string? DeletedBy { get; private set; }
public bool IsDeleted => DeletedBy != null;
// → RN-GLB-002: Toda eliminación es lógica
```

### Patrón: Commands inmutables (CQRS)
```csharp
public record CrearPublicacionCommand(string Titulo, string Contenido, ...);
// → ADR: Inmutabilidad en commands CQRS
```

### Patrón: Auditoría desde JWT
```csharp
// En ApplicationService o Controller
var createdBy = _httpContextAccessor.HttpContext?.User?.FindFirst("sub")?.Value;
// → RN-GLB-004: Auditoría automática desde claims JWT
```

### Patrón: Caché bicapa
```csharp
// MemoryCache primero, luego Redis
if (!_memoryCache.TryGetValue(key, out var cached)) {
    cached = await _redisCache.GetAsync(key);
    if (cached == null) cached = await _cosmosDb.FindAsync(...);
}
// → ADR: Caché de dos niveles L1/L2
```

### Patrón: RabbitMQ con retry/DLQ
```csharp
// En configuración de RabbitMQ
x.UseMessageRetry(r => r.Interval(5, TimeSpan.FromSeconds(5)));
// → ADR: Política de reintentos y Dead-Letter Queue
```

## Extracción de endpoints — formato de tabla

Para cada endpoint extraído, construir una fila:

```
| {SEQ} | {MODULO} | {CONTROLLER} | {NOMBRE-ENDPOINT} | {MÉTODO} | {RUTA} | {DESCRIPCIÓN} | {AUTH} |
```

Ejemplo:
```
| 1 | CRH | Publicacion | Obtener publicaciones paginadas | GET | `/{tenant}/crh/publicacion` | Lista publicaciones activas del tenant con paginación | Cerbos |
| 2 | CRH | Publicacion | Crear publicación | POST | `/{tenant}/crh/publicacion` | Crea nueva publicación en borrador | Cerbos |
```

## Inferir descripción de negocio desde nombres técnicos

| Nombre técnico | Descripción de negocio |
|---|---|
| `GetAll()` con `[HttpGet]` | Listar todos los {recursos} del tenant |
| `GetById(id)` | Obtener el detalle de un {recurso} específico |
| `Create()` con `[HttpPost]` | Crear nuevo {recurso} |
| `Update()` con `[HttpPut]` | Modificar un {recurso} existente |
| `Delete()` | Eliminar (desactivar) un {recurso} |
| `Search()` | Buscar {recursos} por texto o filtros |
| `Export()` | Exportar {recursos} a Excel |
| `GetByTenant()` | Obtener configuración del tenant |
| `GetPagedAsync()` | Lista paginada de {recursos} |
