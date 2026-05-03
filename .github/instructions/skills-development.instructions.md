# Instrucciones — Desarrollo de Skills

## Estructura de un Skill

Cada skill es un directorio con al menos un archivo `instructions.md` que contiene:
- **YAML frontmatter:** `name`, `description`, `model` (opcional), y metadatos de triggering.
- **System prompt:** instrucciones detalladas del comportamiento del skill.

## Convenciones de Naming

- Directorio del skill: `kebab-case` (ej. `crh-comunicacion-interna`)
- Variantes workspace: sufijo `-workspace` (ej. `crh-comunicacion-interna-workspace`)
- Archivos de instrucciones: `instructions.md` como entrada principal

## Descripción del Skill (Triggering)

- La `description` en el frontmatter determina cuándo se activa el skill.
- Incluir frases de activación explícitas ("Use when the user asks to...").
- Incluir frases negativas para evitar falsos positivos ("Do NOT use this skill for...").
- Ser específico: listar los verbos y sustantivos clave que el usuario diría.

## Directorio de Skills

```
.agents/skills/    → Skills de propósito general y CRH
.agent/skills/     → Skills de documentación Workbeat (wbt-doc-*)
```

**⚠️ Gotcha:** `.agents/` ≠ `.agent/` — dos directorios distintos. No confundir.

## Principios de Diseño

- Un skill = un propósito claro y delimitado.
- Preferir output estructurado y predecible.
- Incluir sección de "Resultado Esperado" en el system prompt.
- Si el skill necesita archivos de referencia, documentar las rutas explícitamente.
- Los prompts fuente de CRH están en `F:\WBT\Prompts\prompt_CRH_*.md`.

## Dependencias Externas

- `skills-lock.json` en la raíz del proyecto registra skills externos (fuente: GitHub).
- No modificar manualmente — usar el sistema de gestión de skills (`/skills`).
