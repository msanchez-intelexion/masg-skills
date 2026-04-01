"""
analyze-csharp.py — Workbeat C# Code Analyzer
Extrae información estructural de microservicios Workbeat para generar documentación.

Uso:
  python analyze-csharp.py --src "C:\Microservicios\CRH\src" --output "." --mode summary
  python analyze-csharp.py --src "C:\Microservicios\CRH\src" --output "." --mode controllers
  python analyze-csharp.py --src "C:\Microservicios\CRH\src" --output "." --mode domain
  python analyze-csharp.py --src "C:\Microservicios\CRH\src" --output "." --mode all

Modos:
  summary     - Resumen de controllers, entidades, enums, commands
  controllers - Extrae endpoints de todos los controllers
  domain      - Extrae entidades, commands, value objects y enums
  all         - Ejecuta todos los análisis y genera JSON completo
"""

import os
import re
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Endpoint:
    controller: str
    method: str          # GET, POST, PUT, DELETE, PATCH
    route: str
    action_name: str
    auth_type: str       # Public, JWT, Cerbos
    parameters: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class Entity:
    name: str
    base_class: str
    properties: list[dict] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    file_path: str = ""


@dataclass
class EnumDef:
    name: str
    values: list[str] = field(default_factory=list)
    file_path: str = ""


@dataclass
class CommandDef:
    name: str
    properties: list[dict] = field(default_factory=list)
    file_path: str = ""


def find_files(src_path: str, pattern: str) -> list[Path]:
    """Busca archivos .cs recursivamente."""
    root = Path(src_path)
    return list(root.rglob(pattern))


def extract_auth_type(content: str) -> str:
    """Infiere el tipo de autenticación de un controller o método."""
    if '[AllowAnonymous]' in content:
        return 'Public'
    if '"Cerbos"' in content or "'Cerbos'" in content:
        return 'Cerbos'
    if '[Authorize]' in content:
        return 'JWT'
    return 'Unknown'


def extract_controller_base_route(content: str) -> str:
    """Extrae el Route base del controller."""
    match = re.search(r'\[Route\("([^"]+)"\)\]', content)
    return match.group(1) if match else 'N/A'


def extract_endpoints_from_controller(file_path: Path) -> list[Endpoint]:
    """Extrae todos los endpoints de un archivo Controller."""
    endpoints = []
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return endpoints

    controller_name = file_path.stem.replace('Controller', '')
    base_route = extract_controller_base_route(content)
    controller_auth = extract_auth_type(content[:2000])  # header region

    # Patrón para métodos HTTP en el controller
    http_methods = ['HttpGet', 'HttpPost', 'HttpPut', 'HttpDelete', 'HttpPatch']
    
    # Buscar bloques de método (simplificado)
    method_pattern = re.compile(
        r'\[(Http(?:Get|Post|Put|Delete|Patch))(?:\("([^"]*)"\))?\]'
        r'(?:[^\[]*?\[(Authorize[^\]]*|AllowAnonymous)\])?'
        r'[^\n]*\n\s*(?:public\s+)?(?:async\s+)?(?:Task[^>]*>|ActionResult[^>]*>|IActionResult)\s+'
        r'(\w+)\s*\(',
        re.DOTALL
    )
    
    for match in method_pattern.finditer(content):
        http_verb = match.group(1).replace('Http', '').upper()
        sub_route = match.group(2) or ''
        auth_override = match.group(3) or ''
        action_name = match.group(4)
        
        # Construir ruta completa
        route = base_route
        if sub_route:
            route = f"{route}/{sub_route}".replace('//', '/')
        
        # Determinar auth
        if 'AllowAnonymous' in auth_override:
            auth = 'Public'
        elif 'Cerbos' in auth_override:
            auth = 'Cerbos'
        elif 'Authorize' in auth_override:
            auth = 'JWT'
        else:
            auth = controller_auth
        
        endpoints.append(Endpoint(
            controller=controller_name,
            method=http_verb,
            route=route,
            action_name=action_name,
            auth_type=auth
        ))
    
    return endpoints


def extract_entities(src_path: str) -> list[Entity]:
    """Extrae entidades del dominio."""
    entities = []
    domain_files = find_files(src_path, "*.cs")
    
    # Filtrar archivos de dominio (excluir Commands, Enums, etc.)
    exclude_patterns = ['Command', 'Enum', 'Exception', 'Handler', 'Dto', 'Controller', 'Service']
    
    for file_path in domain_files:
        if any(p in str(file_path) for p in ['Domain', 'domain']):
            if any(p in file_path.name for p in exclude_patterns):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                # Buscar definición de clase que hereda de algo
                class_match = re.search(
                    r'public\s+class\s+(\w+)\s*:\s*(\w+)',
                    content
                )
                if class_match:
                    entity_name = class_match.group(1)
                    base_class = class_match.group(2)
                    
                    # Extraer propiedades públicas
                    props = re.findall(
                        r'public\s+(\S+(?:\?)?)\s+(\w+)\s*\{',
                        content
                    )
                    
                    # Extraer métodos públicos (no propiedades)
                    methods = re.findall(
                        r'public\s+(?:async\s+)?(?:void|Task|string|bool|int|[A-Z]\w+)\s+(\w+)\s*\(',
                        content
                    )
                    
                    entities.append(Entity(
                        name=entity_name,
                        base_class=base_class,
                        properties=[{'type': p[0], 'name': p[1]} for p in props],
                        methods=methods,
                        file_path=str(file_path)
                    ))
            except Exception:
                continue
    
    return entities


def extract_enums(src_path: str) -> list[EnumDef]:
    """Extrae enumeraciones del dominio."""
    enums = []
    for file_path in find_files(src_path, "*.cs"):
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            enum_matches = re.finditer(
                r'public\s+enum\s+(\w+)\s*\{([^}]+)\}',
                content,
                re.DOTALL
            )
            for match in enum_matches:
                enum_name = match.group(1)
                values_raw = match.group(2)
                values = [
                    v.strip().split('=')[0].strip().split('//')[0].strip()
                    for v in values_raw.split(',')
                    if v.strip() and not v.strip().startswith('//')
                ]
                values = [v for v in values if v]
                if values:
                    enums.append(EnumDef(
                        name=enum_name,
                        values=values,
                        file_path=str(file_path)
                    ))
        except Exception:
            continue
    return enums


def extract_commands(src_path: str) -> list[CommandDef]:
    """Extrae Commands CQRS (records con sufijo Command)."""
    commands = []
    for file_path in find_files(src_path, "*.cs"):
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            record_matches = re.finditer(
                r'public\s+record\s+(\w+Command)\s*\(([^)]*)\)',
                content,
                re.DOTALL
            )
            for match in record_matches:
                cmd_name = match.group(1)
                params_raw = match.group(2)
                params = []
                for param in params_raw.split(','):
                    param = param.strip()
                    if param:
                        parts = param.split()
                        if len(parts) >= 2:
                            params.append({'type': parts[-2], 'name': parts[-1]})
                commands.append(CommandDef(
                    name=cmd_name,
                    properties=params,
                    file_path=str(file_path)
                ))
        except Exception:
            continue
    return commands


def generate_summary(src_path: str) -> dict:
    """Genera un resumen estadístico del microservicio."""
    controllers = find_files(src_path, "*Controller.cs")
    endpoints = []
    for c in controllers:
        endpoints.extend(extract_endpoints_from_controller(c))
    
    entities = extract_entities(src_path)
    enums = extract_enums(src_path)
    commands = extract_commands(src_path)
    
    return {
        'controllers': len(controllers),
        'controller_names': [c.stem.replace('Controller', '') for c in controllers],
        'total_endpoints': len(endpoints),
        'endpoints_by_method': {
            m: len([e for e in endpoints if e.method == m])
            for m in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        },
        'endpoints_by_auth': {
            a: len([e for e in endpoints if e.auth_type == a])
            for a in ['Public', 'JWT', 'Cerbos', 'Unknown']
        },
        'entities': len(entities),
        'enums': len(enums),
        'commands': len(commands)
    }


def main():
    parser = argparse.ArgumentParser(description='Workbeat C# Code Analyzer')
    parser.add_argument('--src', required=True, help='Ruta al código fuente (src/)')
    parser.add_argument('--output', default='.', help='Directorio de salida para JSON')
    parser.add_argument('--mode', choices=['summary', 'controllers', 'domain', 'all'],
                       default='summary', help='Modo de análisis')
    args = parser.parse_args()

    src_path = args.src
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Analizando: {src_path}")
    print(f"📁 Salida: {output_path}")
    print(f"⚙️  Modo: {args.mode}")
    print()

    if args.mode in ('summary', 'all'):
        summary = generate_summary(src_path)
        print("📊 RESUMEN:")
        print(f"  Controllers: {summary['controllers']} ({', '.join(summary['controller_names'])})")
        print(f"  Endpoints total: {summary['total_endpoints']}")
        for method, count in summary['endpoints_by_method'].items():
            if count > 0:
                print(f"    {method}: {count}")
        print(f"  Autenticación:")
        for auth, count in summary['endpoints_by_auth'].items():
            if count > 0:
                print(f"    {auth}: {count}")
        print(f"  Entidades del dominio: {summary['entities']}")
        print(f"  Enums: {summary['enums']}")
        print(f"  Commands CQRS: {summary['commands']}")
        
        out_file = output_path / 'analysis-summary.json'
        out_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
        print(f"\n✅ Resumen guardado en: {out_file}")

    if args.mode in ('controllers', 'all'):
        controllers = find_files(src_path, "*Controller.cs")
        all_endpoints = []
        for c in controllers:
            eps = extract_endpoints_from_controller(c)
            all_endpoints.extend([asdict(ep) for ep in eps])
        
        out_file = output_path / 'analysis-controllers.json'
        out_file.write_text(json.dumps(all_endpoints, indent=2, ensure_ascii=False))
        print(f"✅ Controllers guardado en: {out_file} ({len(all_endpoints)} endpoints)")

    if args.mode in ('domain', 'all'):
        entities = [asdict(e) for e in extract_entities(src_path)]
        enums = [asdict(e) for e in extract_enums(src_path)]
        commands = [asdict(c) for c in extract_commands(src_path)]
        
        domain_data = {'entities': entities, 'enums': enums, 'commands': commands}
        out_file = output_path / 'analysis-domain.json'
        out_file.write_text(json.dumps(domain_data, indent=2, ensure_ascii=False))
        print(f"✅ Dominio guardado en: {out_file}")
        print(f"   Entidades: {len(entities)}, Enums: {len(enums)}, Commands: {len(commands)}")

    print("\n🏁 Análisis completo.")


if __name__ == '__main__':
    main()
