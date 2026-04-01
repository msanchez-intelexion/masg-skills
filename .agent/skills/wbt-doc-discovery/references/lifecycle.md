# Ciclo de Vida de Documentación — Referencia Rápida

Documento completo: `F:\WBT\Documentacion_Base\ciclo-vida-documentacion-workbeat.md`

## Las 8 Fases

| Fase | Skill responsable | Entregables clave |
|---|---|---|
| F0 Descubrimiento | `wbt-doc-discovery` | kickoff, brainstorming, JTBD, actores |
| F1 Definición | `wbt-doc-requirements` | visión, casos de uso, reglas de negocio, glosario |
| F2 Diseño | `wbt-doc-design` | arquitectura C4, diagramas de secuencia, flujos UX |
| F3 Construcción | `wbt-doc-reverse-engineer` | SemanticDoc, API Reference, dominio, ADRs |
| F4 Pruebas | `wbt-doc-test-matrix` | matriz básica, matriz extendida, DoD, UAT |
| F5 Release | `wbt-doc-release` | release notes, rollout plan, TTM tracker |
| F6 Capacitación | `wbt-doc-release` | getting started, how-to guides, material por audiencia |
| F7 Soporte | `wbt-doc-release` | runbook, troubleshooting, post-mortems |

## Flujo recomendado: Feature nuevo (F0 → F7)

```
wbt-doc-discovery → wbt-doc-requirements → wbt-doc-design
  → [construcción] → wbt-doc-reverse-engineer → wbt-doc-test-matrix
  → wbt-doc-release (release) → wbt-doc-release (capacitación + soporte)
```

## Flujo recomendado: Ingeniería inversa (código existente)

```
wbt-doc-reverse-engineer (base técnica)
  → wbt-doc-requirements (inferir CU y reglas de negocio)
  → wbt-doc-discovery (actores y JTBD retroactivos)
  → wbt-doc-test-matrix (si se quiere QA)
  → wbt-doc-release (si se quiere capacitar o documentar soporte)
```

## Estructura de carpetas estándar

```
F:\WBT\Documentacion_Base\
├── propuesta-framework-documentacion-workbeat.md
├── ciclo-vida-documentacion-workbeat.md
├── {modulo}\                          ← docs de módulos existentes (CRH, ADM, etc.)
│   ├── SemanticDocumentation.md
│   ├── IndiceMaestroConfiguracion.md
│   ├── arquitectura.md
│   ├── principles.md
│   ├── api\
│   ├── dominio\
│   └── guides\
└── features\                          ← docs de features nuevos o retroactivos
    └── {nombre-feature}\
        ├── 00-kickoff.md ... 12-matriz-cu.md
        ├── casos-de-uso\
        ├── ux\
        ├── diagramas\
        ├── pruebas\
        ├── releases\
        ├── guides\
        ├── capacitacion\
        └── soporte\
```

## Módulos de Workbeat y sus abreviaturas

| Módulo | Abreviatura | Ruta código | Prefijo RN | Prefijo CU |
|---|---|---|---|---|
| Administración (CoreRH) | ADM | `C:\Microservicios\ADM\` | `RN-ADM-` | `CU-ADM-` |
| Comunicación RH | CRH | `C:\Microservicios\CRH\` | `RN-CRH-` | `CU-CRH-` |
| Nómina | NOM | `C:\Microservicios\NOM\` | `RN-NOM-` | `CU-NOM-` |
| Asistencia | ASIST | `C:\Microservicios\ASIST\` | `RN-AST-` | `CU-AST-` |
| Talento | TALENT | `C:\Microservicios\TALENT\` | `RN-TAL-` | `CU-TAL-` |
| Employee Experience | EX | `C:\Microservicios\EX\` | `RN-EX-` | `CU-EX-` |
| Global/Transversal | GLB | — | `RN-GLB-` | `CU-GLB-` |
