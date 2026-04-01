# Caso de Uso: {ID} — {Nombre del Caso de Uso}

> **ID:** `CU-{MODULO}-{NNN}`  
> **Feature:** {nombre del feature}  
> **Módulo Workbeat:** {ADM | CRH | NOM | ASIST | TALENT | EX}  
> **Versión:** 1.0

---

## Descripción

{Una oración que describe el objetivo del actor con este caso de uso.}

## Actores

| Rol | Actor | Tipo |
|---|---|---|
| Principal | {nombre del actor} | Humano / Sistema |
| Secundario | {nombre del actor} | Humano / Sistema |

## Precondiciones específicas

1. {Estado que debe cumplirse antes de iniciar este caso de uso.}
2. {Puede referenciar una precondición global: ver `09-precondiciones.md`.}

## Flujo Principal (Happy Path)

| Paso | Actor | Acción |
|---|---|---|
| 1 | {Actor} | {acción concreta y observable} |
| 2 | Sistema | {respuesta del sistema} |
| 3 | {Actor} | {siguiente acción} |
| 4 | Sistema | {respuesta final} |

## Flujos Alternativos

### Alternativa A — {Nombre del escenario alternativo}

> Se activa en el paso {N} cuando {condición}.

| Paso | Actor | Acción |
|---|---|---|
| {N}A.1 | Sistema | {qué hace el sistema} |
| {N}A.2 | {Actor} | {qué hace el actor} |

El caso de uso {continúa desde el paso N+1 | termina}.

## Flujos de Error / Excepción

### Error E1 — {Nombre del error}

> Se activa en el paso {N} cuando {condición de falla}.

| Paso | Actor | Acción |
|---|---|---|
| {N}E.1 | Sistema | Muestra mensaje: "{texto del error en lenguaje de negocio}" |

**El caso de uso termina.** El actor puede {qué puede hacer para continuar}.

## Postcondiciones

- {Estado del sistema después de que el caso de uso termina exitosamente.}
- {Ejemplo: "El saldo de vacaciones del empleado se actualiza."}

## Reglas de Negocio Aplicadas

| ID | Regla |
|---|---|
| `RN-{MOD}-{NNN}` | {descripción breve} |

## Notas de UX

- {Consideraciones de experiencia de usuario relevantes para este flujo.}
- {Ejemplo: "En paso 3, mostrar contador de caracteres restantes."}

## Trazabilidad

- **Escenarios de prueba:** `TP-{MOD}-{NNN}` (ver `pruebas/matriz-pruebas.md`)
- **Reglas de negocio:** ver `10-reglas-de-negocio.md`
- **Mockup:** ver `ux/mockups.md`

---
> 📋 Documento de Fase 1 — Caso de Uso | Workbeat Documentation Lifecycle
