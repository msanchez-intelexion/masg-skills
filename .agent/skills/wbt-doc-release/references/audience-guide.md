# Guía de Audiencias — Tono y Contenido por Tipo de Usuario

## Principios generales

- **Empleado final:** Nunca usar términos técnicos. Hablar de "tu expediente", "tus días disponibles", "tu solicitud".
- **Jefe directo:** Términos de negocio ("equipo", "aprobación", "reporte"), sin código ni términos de sistema.
- **Admin RH:** Términos de configuración ("catálogo", "regla", "plantilla"), puede ver números de campos.
- **Integrador técnico:** Términos técnicos completos. Incluir ejemplos de código, URLs exactas, JSON.
- **Soporte L1:** Orientado a síntoma→solución. Sin contexto de por qué, solo qué hacer.
- **Agente IA:** Exhaustivo, estructurado, técnico. Todo el contexto posible.

## Vocabulario por audiencia

| Concepto técnico | Empleado | Admin RH | Integrador |
|---|---|---|---|
| Tenant | Tu empresa | Tu organización / tenant | Tenant GUID |
| JWT token | Tu sesión | Sesión del usuario | Bearer Token JWT |
| Endpoint | — | — | `POST /api/v1/{tenant}/crh/publicacion` |
| CosmosDB | — | Base de datos | Azure CosmosDB (partition key: `{año}-{tenant}`) |
| Soft delete | Elemento eliminado | Registro desactivado | `DeletedBy` ≠ null |
| Cerbos | — | Permisos del sistema | Política Cerbos en header Authorization |
| RabbitMQ | — | Notificaciones automáticas | Evento en RabbitMQ queue |
| Redis cache | — | Datos en caché | Redis L2 cache |

## Estructura de materiales por audiencia

### Empleado final
```markdown
# {Nombre de la funcionalidad} — Guía rápida

**¿Qué puedes hacer?** {1 oración simple}

## Cómo hacerlo
1. Abre {nombre de la app/sección}
2. Toca / haz clic en "{nombre del botón}"
3. {acción simple}
4. ¡Listo! {resultado}

## ¿Algo no funcionó?
Contacta a tu área de Recursos Humanos o escríbenos a {contacto}.
```

### Administrador RH
```markdown
# Configurar {funcionalidad} — Guía para administradores

**Prerequisitos:** {qué debe estar configurado antes}

## Configuración inicial
1. Ir a {módulo} → {sección}
2. {paso con nombre exacto del campo}
3. Guardar cambios

## Gestión diaria
{cómo usar la funcionalidad en operación}

## Reportes disponibles
{qué puede exportar/ver}

## Preguntas frecuentes
```

### Integrador técnico
```markdown
# Integración con {funcionalidad} — API Reference

**URL base:** `api/v1/{tenant:guid}/{módulo}/{recurso}`
**Autenticación:** Bearer Token JWT (IdentityServer4)
**Autorización:** Política Cerbos requerida

## Endpoints
{tabla completa con método, ruta, descripción, auth}

## Ejemplos de request/response
{JSON completo con datos ficticios pero realistas}

## Errores
{tabla de códigos HTTP y su significado de negocio}

## Colección de Postman
{link o instrucciones para importar}
```

## Longitud recomendada por tipo de documento

| Documento | Audiencia | Palabras máx. |
|---|---|---|
| Getting Started | Todos | 400 |
| How-to guía | Empleado | 300 |
| How-to guía | Admin RH | 700 |
| How-to guía | Integrador | Sin límite |
| Resumen ejecutivo | Líderes | 350 |
| Release notes (usuario) | Empleado | 200 |
| Release notes (técnicas) | Integrador | Sin límite |
| Runbook | Soporte | 800-1200 |
| SemanticDocumentation | Agente IA | Sin límite |
