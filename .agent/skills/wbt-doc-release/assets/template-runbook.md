# Runbook Operacional — {NOMBRE DEL FEATURE}

> **Módulo:** {ADM | CRH | NOM | ASIST | TALENT | EX}  
> **Versión:** {X.Y.Z}  
> **Equipo responsable:** {equipo}  
> **Escalada a:** {contacto o equipo senior}  
> **SLA respuesta P0:** {tiempo}

---

## Verificación de salud

```powershell
# Health check del microservicio
Invoke-RestMethod -Uri "https://{env}.workbeat.com/api/v1/values" -Method GET

# Verificar mensajes en Dead-Letter Queue
# (RabbitMQ Management UI: http://{rabbitmq-host}:15672)
# Queue: {nombre-dlq}

# Verificar estado de Redis
# redis-cli -h {redis-host} ping
```

---

## Síntomas comunes y diagnóstico

### 🔴 Síntoma: {descripción del problema — qué ve el usuario}

**Causa probable:** {causa técnica}

**Diagnóstico paso a paso:**
1. Verificar logs en Application Insights:
   ```kql
   traces
   | where timestamp > ago(1h)
   | where message contains "{término clave}"
   | order by timestamp desc
   | take 50
   ```
2. Verificar DLQ en RabbitMQ: `{nombre de la queue}`
3. Verificar partition key en CosmosDB: `{año}-{tenantId}`

**Resolución:**
1. {paso 1 de resolución}
2. {paso 2}

**Cuándo escalar:** Si el síntoma persiste más de {N} minutos o afecta a más de {N} tenants.

---

### 🟡 Síntoma: {otro síntoma}

**Causa probable:** {causa}

**Diagnóstico:**
```kql
exceptions
| where timestamp > ago(2h)
| where type contains "{tipo de excepción}"
| summarize count() by type, outerMessage
```

**Resolución:** {pasos}

---

## Procedimiento de rollback

```powershell
# Si se requiere rollback a la versión anterior
# 1. Desactivar feature flag en {sistema de configuración}
# 2. Notificar al equipo en {canal de Slack/Teams}
# 3. Documentar en {sistema de incidencias}
```

---

## Contactos de escalada

| Nivel | Contacto | Cuándo escalar |
|---|---|---|
| L1 | {Soporte helpdesk} | Error reportado por usuario |
| L2 | {Equipo técnico del módulo} | Error técnico no resuelto en 30min |
| L3 | {Arquitecto / Tech Lead} | P0, pérdida de datos, falla regulatoria |

---
> 📋 Documento de Fase 7 — Runbook | Workbeat Documentation Lifecycle
