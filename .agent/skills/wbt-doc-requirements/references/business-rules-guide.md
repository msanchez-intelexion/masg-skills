# Guía de Reglas de Negocio — Convenciones Workbeat

## Convención de IDs

Formato: `RN-{MODULO}-{NNN}` donde NNN es número de 3 dígitos con ceros a la izquierda.

| Módulo | Código | Ejemplo |
|---|---|---|
| ADM (CoreRH) | ADM | `RN-ADM-001` |
| CRH (Comunicación) | CRH | `RN-CRH-001` |
| NOM (Nómina) | NOM | `RN-NOM-001` |
| ASIST (Asistencia) | AST | `RN-AST-001` |
| TALENT | TAL | `RN-TAL-001` |
| EX (Employee Experience) | EX | `RN-EX-001` |
| Global / Transversal | GLB | `RN-GLB-001` |

## Reglas Globales de Workbeat (ya definidas — no duplicar)

Estas reglas aplican a TODOS los módulos:

| ID | Regla | Origen |
|---|---|---|
| `RN-GLB-001` | El `id` de todo documento en CosmosDB debe estar en minúsculas | Técnico |
| `RN-GLB-002` | Toda eliminación es lógica (soft delete) — nunca física | Técnico |
| `RN-GLB-003` | Toda query debe incluir la partition key `{Año}-{TenantId}` | Técnico |
| `RN-GLB-004` | Los campos `CreatedBy/UpdatedBy/DeletedBy` se extraen del JWT, no se pasan manualmente | Técnico |
| `RN-GLB-005` | Los datos de un tenant nunca son visibles para otro tenant | Negocio/Seguridad |
| `RN-GLB-006` | La autenticación es mediante JWT emitido por IdentityServer4 | Técnico |
| `RN-GLB-007` | La autorización en controllers usa política Cerbos excepto endpoints públicos | Técnico |
| `RN-GLB-008` | Los datos de empleados se protegen bajo LFPDPPP (Ley Federal de Protección de Datos) | Regulatorio |

## Categorías de origen de reglas de negocio

| Origen | Descripción | Ejemplos |
|---|---|---|
| **Regulatorio** | Impuesto por ley, norma o regulación | SAT, IMSS, Infonavit, LFPDPPP |
| **Negocio** | Decisión de producto/empresa | "Solo 1 posición activa por empleado" |
| **Técnico** | Restricción de la arquitectura | "IDs en minúsculas en CosmosDB" |

## Estructura de tabla de reglas de negocio

```markdown
| ID | Regla | Origen | Módulo(s) | Excepción | Referencia |
|---|---|---|---|---|---|
| RN-CRH-001 | Una publicación debe pertenecer a exactamente un canal | Negocio | CRH | — | CU-CRH-001 |
| RN-NOM-001 | El CFDI debe timbrase ≤72h después de la dispersión | Regulatorio SAT | NOM | Contingencia SAT | Art. 29 CFF |
```

## Cómo inferir reglas desde código (ingeniería inversa)

Buscar en el código:

1. **Validaciones en constructores de entidades** → Reglas de negocio invariantes
   ```csharp
   // Si el constructor valida, es una regla de negocio
   if (string.IsNullOrWhiteSpace(titulo)) throw new DomainException("...");
   ```

2. **Guards en ApplicationService** → Precondiciones y reglas
   ```csharp
   if (empleado.Status != EmpleadoStatus.Activo) throw new BusinessRuleException("...");
   ```

3. **Atributos `[Required]`, `[MaxLength]`, `[Range]`** → Reglas de validación de formato

4. **Constantes y enums** → Valores permitidos (= reglas de dominio)

5. **Comentarios `// RN-XXX-NNN`** → Si el equipo ya usaba esta convención
