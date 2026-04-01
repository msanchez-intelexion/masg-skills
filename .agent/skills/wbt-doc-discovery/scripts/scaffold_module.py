"""
scaffold_module.py — Crea la estructura de carpetas de documentación para un módulo Workbeat.

Uso:
    python scaffold_module.py --module CRH
    python scaffold_module.py --module ADM --base-path "F:\\WBT\\Microservicios"
    python scaffold_module.py --module ONB --list-only

Requiere Python 3.8+. Sin dependencias externas.
"""

import argparse
import json
import os
import sys

# ──────────────────────────────────────────────────────────────────────────────
# Registro de módulos
# ──────────────────────────────────────────────────────────────────────────────
MODULES = {
    "CRH": {
        "name": "Comunicación RH",
        "base_path": r"F:\WBT\Microservicios\ComunicacionRH",
        "functionalities": [
            ("dashboard",               "DASH", "Panel de control de publicaciones y métricas"),
            ("publicaciones",           "PUB",  "Listado, expediente y gestión de publicaciones"),
            ("creacion-publicaciones",  "WIZ",  "Wizard de creación con IA y editor de contenido"),
            ("editores",                "EDT",  "Gestión de roles de editor"),
            ("revisores",               "REV",  "Flujo de revisión y aprobación"),
            ("campanas",                "CAM",  "Campañas de comunicación"),
            ("canales-y-notificaciones","NOT",  "Configuración de canales y despacho de notificaciones"),
            ("configuracion",           "CFG",  "Configuración del tenant y del módulo"),
            ("comentarios",             "COM",  "Gestión de comentarios en publicaciones"),
            ("palabras-especiales",     "PAL",  "Filtro de palabras altisonantes"),
            ("espacios-digitales",      "ESP",  "Employee Apps / Espacios de contenido"),
            ("filtros-y-segmentacion",  "FIL",  "Segmentación de audiencia para publicaciones"),
            ("avisos",                  "AVI",  "Avisos y alertas del sistema"),
            ("reportes",                "REP",  "Exportación y reportes del módulo"),
        ],
    },
    "ADM": {
        "name": "Core RH / Administración",
        "base_path": r"F:\WBT\Microservicios\CoreRH",
        "functionalities": [
            ("alta-empleados",          "ALTA", "Proceso de incorporación de nuevos empleados"),
            ("baja-empleados",          "BAJA", "Proceso de desvinculación de empleados"),
            ("movimientos",             "MOV",  "Cambios de posición, promociones y transferencias"),
            ("expediente-empleado",     "EXP",  "Ficha completa del empleado"),
            ("estructura-organizacional","EST", "Razones sociales, organizaciones y jerarquía"),
            ("posiciones",              "POS",  "Posiciones y descripciones de puesto"),
            ("procesos",                "PROC", "Flujos configurables: etapas, pasos y actividades"),
            ("configuracion",           "CFG",  "Comportamientos y parámetros del sistema"),
            ("dashboard",               "DASH", "Panel de control de indicadores RH"),
            ("directorio-corporativo",  "DIR",  "Vista pública del directorio de empleados"),
            ("catalogos-gubernamentales","CAT", "Catálogos SAT, IMSS, Infonavit"),
            ("motivos-de-baja",         "MOT",  "Catálogo de razones de terminación"),
            ("integraciones-ia",        "IA",   "Funcionalidades con inteligencia artificial"),
        ],
    },
    "ONB": {
        "name": "Incorporación / Onboarding",
        "base_path": r"F:\WBT\Microservicios\Incorporacion_Onboarding",
        "functionalities": [
            ("proceso-incorporacion",   "PROC", "Flujo principal del proceso de onboarding"),
            ("etapas-y-pasos",          "ETAP", "Configuración de etapas, pasos y actividades"),
            ("actividades",             "ACT",  "Actividades asignadas al nuevo colaborador"),
            ("documentos-y-firmas",     "DOC",  "Carga y firma electrónica de documentos"),
            ("autenticacion-mfa",       "MFA",  "Verificación de identidad multifactor"),
            ("notificaciones",          "NOT",  "Comunicaciones automáticas durante el proceso"),
            ("portal-candidato",        "PORT", "Experiencia del futuro empleado en el portal"),
            ("configuracion",           "CFG",  "Parámetros del proceso por tenant"),
            ("dashboard",               "DASH", "Seguimiento y métricas del proceso de incorporación"),
        ],
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# Plantillas de archivos README
# ──────────────────────────────────────────────────────────────────────────────
MODULE_README_TEMPLATE = """\
# {module_name} — Documentación del módulo

> **Código:** `{module_code}`  
> **Ruta:** `{base_path}`  
> **Estructura:** [organización-documentacion-por-funcionalidad.md](F:\\WBT\\Documentacion_Base\\organizacion-documentacion-por-funcionalidad.md)

## Funcionalidades

| Funcionalidad | Código | Carpeta | Descripción |
|---|---|---|---|
{rows}

## Documentación transversal

Ver `_transversal/` para:
- `SemanticDocumentation.md` — visión general del módulo
- `arquitectura.md` — arquitectura técnica
- `glosario.md` — términos del dominio
- `reglas-negocio-globales.md` — reglas transversales (prefijo `RN-{module_code}-GLB-`)
- `actores.md` — actores y meta-personas
- `precondiciones-globales.md` — pre-condiciones compartidas

---
*Generado con `scaffold_module.py` — Workbeat Documentation Framework*
"""

FUNC_README_TEMPLATE = """\
# {func_display} — {module_name}

> **Módulo:** `{module_code}` | **Funcionalidad:** `{func_code}`  
> **Ruta:** `{func_path}`

## Descripción

{description}

## Artefactos de documentación

| Directorio/Archivo | Contenido | Prefijo de ID |
|---|---|---|
| `casos-de-uso/` | Narrativas de caso de uso | `CU-{module_code}-{func_code}-NNN` |
| `reglas-de-negocio/` | Reglas de negocio específicas | `RN-{module_code}-{func_code}-NNN` |
| `matriz-de-pruebas/` | Casos de prueba y escenarios | `TP-{module_code}-{func_code}-NNN` |
| `diagramas/` | Flujo, secuencia, C4 | — |
| `ux/` | Wireframes y flujo de pantallas | — |
| `vision-general.md` | Descripción ejecutiva | — |
| `glosario.md` | Términos específicos | — |

## Estado

| Fase | Artefacto | Estado |
|---|---|---|
| F0 Discovery | Kickoff, JTBD | ❌ Pendiente |
| F1 Requirements | Casos de uso, RN | ❌ Pendiente |
| F2 Design | Diagramas, UX | ❌ Pendiente |
| F4 Testing | Matriz de pruebas | ❌ Pendiente |
| F5-F7 Release | Notas de versión, guías | ❌ Pendiente |

---
*Generado con `scaffold_module.py` — Workbeat Documentation Framework*
"""

TRANSVERSAL_README = """\
# _transversal — Documentación transversal del módulo {module_name}

Esta carpeta contiene artefactos que aplican a **todo el módulo** y que son referenciados
por las documentaciones de cada funcionalidad individual.

## Archivos esperados

| Archivo | Descripción | Estado |
|---|---|---|
| `SemanticDocumentation.md` | Visión general semántica del módulo | ❌ Pendiente |
| `arquitectura.md` | Arquitectura técnica del módulo | ❌ Pendiente |
| `glosario.md` | Términos y definiciones del dominio | ❌ Pendiente |
| `actores.md` | Actores del sistema y meta-personas | ❌ Pendiente |
| `reglas-negocio-globales.md` | Reglas de negocio transversales (`RN-{module_code}-GLB-`) | ❌ Pendiente |
| `precondiciones-globales.md` | Pre-condiciones compartidas entre funcionalidades | ❌ Pendiente |
| `roles-y-permisos.md` | Matriz de roles y permisos del módulo | ❌ Pendiente |
| `configuracion-index.md` | Índice de configuraciones disponibles por tenant | ❌ Pendiente |
| `integraciones.md` | Integraciones con otros módulos y sistemas externos | ❌ Pendiente |

---
*Generado con `scaffold_module.py` — Workbeat Documentation Framework*
"""


def create_func_dirs(func_path: str):
    """Crea los subdirectorios estándar dentro de una carpeta de funcionalidad."""
    subdirs = ["_assets", "casos-de-uso", "reglas-de-negocio", "matriz-de-pruebas", "diagramas", "ux"]
    for sub in subdirs:
        os.makedirs(os.path.join(func_path, sub), exist_ok=True)


def scaffold_module(module_code: str, override_base: str = None, list_only: bool = False):
    """Crea la estructura completa de documentación para un módulo."""
    if module_code.upper() not in MODULES:
        print(f"❌ Módulo '{module_code}' no encontrado. Disponibles: {', '.join(MODULES.keys())}")
        sys.exit(1)

    cfg = MODULES[module_code.upper()]
    base = override_base if override_base else cfg["base_path"]
    name = cfg["name"]
    funcs = cfg["functionalities"]

    if list_only:
        print(f"\n📦 Módulo: {name} ({module_code.upper()})")
        print(f"   Base: {base}")
        print(f"\n   Funcionalidades ({len(funcs)}):")
        for folder, code, desc in funcs:
            print(f"   ├─ {folder:30s} [{code}]  {desc}")
        print(f"   └─ _transversal/ (docs transversales)")
        return

    print(f"\n🚀 Scaffolding módulo: {name} ({module_code.upper()})")
    print(f"   Ruta base: {base}\n")

    # Directorio raíz del módulo
    os.makedirs(base, exist_ok=True)

    # _transversal
    trans_path = os.path.join(base, "_transversal")
    os.makedirs(trans_path, exist_ok=True)
    trans_readme = os.path.join(trans_path, "README.md")
    if not os.path.exists(trans_readme):
        with open(trans_readme, "w", encoding="utf-8") as f:
            f.write(TRANSVERSAL_README.format(module_name=name, module_code=module_code.upper()))
        print(f"   ✅ _transversal/README.md")
    else:
        print(f"   ⏭  _transversal/README.md ya existe, omitido")

    # Funcionalidades
    rows = []
    for folder, code, desc in funcs:
        func_path = os.path.join(base, folder)
        os.makedirs(func_path, exist_ok=True)
        create_func_dirs(func_path)

        readme_path = os.path.join(func_path, "README.md")
        if not os.path.exists(readme_path):
            content = FUNC_README_TEMPLATE.format(
                func_display=folder.replace("-", " ").title(),
                module_name=name,
                module_code=module_code.upper(),
                func_code=code,
                func_path=func_path,
                description=desc,
            )
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   ✅ {folder}/README.md")
        else:
            print(f"   ⏭  {folder}/README.md ya existe, omitido")

        rows.append(f"| {folder.replace('-', ' ').title()} | `{code}` | `{folder}/` | {desc} |")

    # README raíz del módulo
    root_readme = os.path.join(base, "README.md")
    if not os.path.exists(root_readme):
        content = MODULE_README_TEMPLATE.format(
            module_name=name,
            module_code=module_code.upper(),
            base_path=base,
            rows="\n".join(rows),
        )
        with open(root_readme, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   ✅ README.md (raíz)")
    else:
        print(f"   ⏭  README.md (raíz) ya existe, omitido")

    print(f"\n✅ Módulo '{name}' scaffoldeado en: {base}")


def main():
    parser = argparse.ArgumentParser(description="Scaffold de documentación de módulos Workbeat")
    parser.add_argument("--module", required=True, help="Código del módulo (CRH, ADM, ONB, ...)")
    parser.add_argument("--base-path", help="Sobreescribe la ruta base del módulo")
    parser.add_argument("--list-only", action="store_true", help="Solo muestra la estructura, no crea archivos")
    args = parser.parse_args()

    scaffold_module(args.module, args.base_path, args.list_only)


if __name__ == "__main__":
    main()
