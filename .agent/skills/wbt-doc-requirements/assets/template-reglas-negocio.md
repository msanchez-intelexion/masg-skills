# Reglas de Negocio — {NOMBRE DEL FEATURE}

> **Feature:** {nombre}  
> **Módulo:** {ADM | CRH | NOM | ASIST | TALENT | EX}  
> **Fecha:** {YYYY-MM-DD}  
> **Versión:** 1.0

---

## Precondición

Las reglas globales de Workbeat (`RN-GLB-001` a `RN-GLB-008`) aplican a este feature.
Ver `references/business-rules-guide.md` para la lista completa.

---

## Reglas de Negocio del Feature

| ID | Regla | Origen | Módulo | Excepción | Referencia |
|---|---|---|---|---|---|
| `RN-{MOD}-001` | {Enunciado de la regla en lenguaje de negocio} | Regulatorio / Negocio / Técnico | {módulo} | {si la hay} | {CU-ID o ley o artículo} |
| `RN-{MOD}-002` | | | | | |

---

## Reglas Regulatorias (si aplica)

> Completar solo si el feature toca regulaciones mexicanas.

| Regulación | Artículo / Norma | Impacto en el feature |
|---|---|---|
| SAT — CFF Art. 29 | Timbrado CFDI ≤72h | Validar en servicio de timbrado |
| IMSS — LSS Art. XX | | |
| Infonavit | | |
| LFPDPPP | | Datos personales con consentimiento |

---

## Matriz de Reglas × Casos de Uso

| Regla | CU que la aplica |
|---|---|
| `RN-{MOD}-001` | `CU-{MOD}-001`, `CU-{MOD}-003` |

---
> 📋 Documento de Fase 1 — Reglas de Negocio | Workbeat Documentation Lifecycle
