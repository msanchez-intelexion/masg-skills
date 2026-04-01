<# 
.SYNOPSIS
Crea la estructura de carpetas de documentación para un módulo Workbeat.

.EXAMPLE
.\scaffold_module.ps1 -Module CRH
.\scaffold_module.ps1 -Module ADM -BasePath "F:\WBT\Microservicios\CoreRH"
.\scaffold_module.ps1 -Module ONB -ListOnly
#>
param(
    [Parameter(Mandatory)][ValidateSet("CRH","ADM","ONB","NOM","ASIST","TALENT","EX")]
    [string]$Module,
    [string]$BasePath,
    [switch]$ListOnly
)

# Registro de módulos
$MODULES = @{
    "CRH" = @{
        Name = "Comunicación RH"
        DefaultPath = "F:\WBT\Microservicios\ComunicacionRH"
        Functionalities = @(
            @("dashboard","DASH","Panel de control de publicaciones y métricas"),
            @("publicaciones","PUB","Listado, expediente y gestión de publicaciones"),
            @("creacion-publicaciones","WIZ","Wizard de creación con IA y editor de contenido"),
            @("editores","EDT","Gestión de roles de editor"),
            @("revisores","REV","Flujo de revisión y aprobación"),
            @("campanas","CAM","Campañas de comunicación"),
            @("canales-y-notificaciones","NOT","Configuración de canales y despacho de notificaciones"),
            @("configuracion","CFG","Configuración del tenant y del módulo"),
            @("comentarios","COM","Gestión de comentarios en publicaciones"),
            @("palabras-especiales","PAL","Filtro de palabras altisonantes"),
            @("espacios-digitales","ESP","Employee Apps / Espacios de contenido"),
            @("filtros-y-segmentacion","FIL","Segmentación de audiencia para publicaciones"),
            @("avisos","AVI","Avisos y alertas del sistema"),
            @("reportes","REP","Exportación y reportes del módulo")
        )
    }
    "ADM" = @{
        Name = "Core RH"
        DefaultPath = "F:\WBT\Microservicios\CoreRH"
        Functionalities = @(
            @("alta-empleados","ALTA","Proceso de incorporación de nuevos empleados"),
            @("baja-empleados","BAJA","Proceso de desvinculación de empleados"),
            @("movimientos","MOV","Cambios de posición, promociones y transferencias"),
            @("expediente-empleado","EXP","Ficha completa del empleado"),
            @("estructura-organizacional","EST","Razones sociales, organizaciones y jerarquía"),
            @("posiciones","POS","Posiciones y descripciones de puesto"),
            @("procesos","PROC","Flujos configurables: etapas, pasos y actividades"),
            @("configuracion","CFG","Comportamientos y parámetros del sistema"),
            @("dashboard","DASH","Panel de control de indicadores RH"),
            @("directorio-corporativo","DIR","Vista pública del directorio de empleados"),
            @("catalogos-gubernamentales","CAT","Catálogos SAT, IMSS, Infonavit"),
            @("motivos-de-baja","MOT","Catálogo de razones de terminación"),
            @("integraciones-ia","IA","Funcionalidades con inteligencia artificial")
        )
    }
    "ONB" = @{
        Name = "Incorporación / Onboarding"
        DefaultPath = "F:\WBT\Microservicios\Incorporacion_Onboarding"
        Functionalities = @(
            @("proceso-incorporacion","PROC","Flujo principal del proceso de onboarding"),
            @("etapas-y-pasos","ETAP","Configuración de etapas, pasos y actividades"),
            @("actividades","ACT","Actividades asignadas al nuevo colaborador"),
            @("documentos-y-firmas","DOC","Carga y firma electrónica de documentos"),
            @("autenticacion-mfa","MFA","Verificación de identidad multifactor"),
            @("notificaciones","NOT","Comunicaciones automáticas durante el proceso"),
            @("portal-candidato","PORT","Experiencia del futuro empleado en el portal"),
            @("configuracion","CFG","Parámetros del proceso por tenant"),
            @("dashboard","DASH","Seguimiento y métricas del proceso de incorporación")
        )
    }
}

$cfg = $MODULES[$Module]
$base = if ($BasePath) { $BasePath } else { $cfg.DefaultPath }
$name = $cfg.Name

if ($ListOnly) {
    Write-Host "`n📦 Módulo: $name ($Module)" -ForegroundColor Cyan
    Write-Host "   Base: $base"
    $cfg.Functionalities | ForEach-Object { Write-Host ("   ├─ {0,-32} [{1}]  {2}" -f $_[0], $_[1], $_[2]) }
    Write-Host "   └─ _transversal/"
    return
}

Write-Host "`n🚀 $name ($Module) → $base" -ForegroundColor Cyan

# _transversal
$transPath = Join-Path $base "_transversal"
New-Item -ItemType Directory -Path $transPath -Force | Out-Null
$transReadme = Join-Path $transPath "README.md"
if (-not (Test-Path $transReadme)) {
    "# _transversal — $name`n`nDocumentos transversales a todo el módulo.`n`nVer ``registro-modulos-workbeat.md`` para estructura esperada." |
        Set-Content $transReadme -Encoding UTF8
    Write-Host "   ✅ _transversal/README.md"
}

# Funcionalidades
foreach ($f in $cfg.Functionalities) {
    $folder, $code, $desc = $f
    $funcPath = Join-Path $base $folder
    @("","_assets","casos-de-uso","reglas-de-negocio","matriz-de-pruebas","diagramas","ux") |
        ForEach-Object { New-Item -ItemType Directory -Path (Join-Path $funcPath $_) -Force | Out-Null }
    $readme = Join-Path $funcPath "README.md"
    if (-not (Test-Path $readme)) {
        "# $folder — $name`n`n**Código:** ``$Module-$code``  `n**Descripción:** $desc" |
            Set-Content $readme -Encoding UTF8
        Write-Host "   ✅ $folder/README.md"
    } else {
        Write-Host "   ⏭  $folder (ya existe)"
    }
}
Write-Host "`n✅ Scaffold completado." -ForegroundColor Green
