# Matriz de Pruebas Básica — {NOMBRE DEL FEATURE}

> **Feature:** {nombre}  
> **Módulo:** {ADM | CRH | NOM | ASIST | TALENT | EX}  
> **Versión:** {X.Y.Z}  
> **Fecha:** {YYYY-MM-DD}  
> **Tester:** {nombre}

---

## Resumen de cobertura

| Total casos | ✅ Aprobados | ❌ Fallidos | 🔄 Pendientes | ⏭️ Bloqueados | % Aprobación |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | — |

---

## Casos de Prueba

| ID | Caso de prueba | Tipo | Actor | Precondición | Pasos (resumen) | Entrada | Resultado esperado | Resultado real | Estado | CU trazado |
|---|---|---|---|---|---|---|---|---|---|---|
| `TP-{MOD}-001` | Happy path principal | Funcional | {Actor} | {precondición} | 1. {paso} 2. {paso} | `{datos}` | `{respuesta esperada}` | — | 🔄 | `CU-{MOD}-001` |
| `TP-{MOD}-001E` | Error: {nombre error} | Funcional | {Actor} | {precondición} | | `{datos inválidos}` | Error 422: {mensaje} | — | 🔄 | `CU-{MOD}-001` |
| `TP-SEC-001` | JWT expirado | Seguridad | Sistema | Token expirado | Enviar request con token vencido | Bearer exp=pasado | 401 Unauthorized | — | 🔄 | — |
| `TP-SEC-002` | Tenant isolation | Seguridad | Sistema | 2 tenants distintos | Tenant A accede recurso de Tenant B | tenant_b_id en URL | 403 o 404 | — | 🔄 | — |
| `TP-SEC-003` | IDOR | Seguridad | Sistema | Recurso de otro usuario | Usar ID ajeno en URL | id_ajeno | 403 o 404 | — | 🔄 | — |
| `TP-SEC-004` | Sin Authorization header | Seguridad | Sistema | — | Request sin header | Sin Bearer | 401 Unauthorized | — | 🔄 | — |
| `TP-SEC-005` | Cerbos sin permiso | Seguridad | Empleado sin rol | JWT válido, sin política | Llamar endpoint protegido | Bearer válido, rol insuf. | 403 Forbidden | — | 🔄 | — |

---

## Leyenda de estados

| Estado | Significado |
|---|---|
| 🔄 Pendiente | No ejecutado |
| ✅ Aprobado | Ejecutado y pasa |
| ❌ Fallido | Ejecutado y falla |
| ⏭️ Bloqueado | No se puede ejecutar por dependencia |
| ⚠️ Parcial | Pasa con observaciones |

---
> 📋 Documento de Fase 4 — Matriz de Pruebas Básica | Workbeat Documentation Lifecycle
