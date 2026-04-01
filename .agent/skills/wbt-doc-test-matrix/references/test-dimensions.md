# Dimensiones de Prueba — Referencia Workbeat

## Dimensión 1: Valores Límite (Boundary Values)

Para cada campo de entrada, probar:

| Escenario | Entrada | Resultado esperado |
|---|---|---|
| Vacío / Null | `null` o `""` | Error 422 con mensaje descriptivo |
| Mínimo exacto | Valor = límite inferior | Éxito |
| Máximo exacto | Valor = límite superior | Éxito |
| Sobre el máximo | Valor = límite superior + 1 | Error 422 |
| Negativo (si numérico) | `-1` | Error 422 |

## Dimensión 2: Seguridad — Casos Obligatorios en Workbeat

Estos 5 casos son **obligatorios en todos los features**:

| ID | Caso | Entrada | Esperado |
|---|---|---|---|
| `TP-SEC-001` | JWT expirado | Bearer token con `exp` en el pasado | 401 Unauthorized |
| `TP-SEC-002` | Tenant isolation | Tenant A accede recurso de Tenant B | 403 Forbidden o 404 |
| `TP-SEC-003` | IDOR | ID de recurso perteneciente a otro usuario en la URL | 403 o 404 |
| `TP-SEC-004` | Sin header Authorization | Request sin `Authorization` header | 401 Unauthorized |
| `TP-SEC-005` | Cerbos sin permiso | JWT válido pero usuario sin política Cerbos | 403 Forbidden |

Casos adicionales recomendados:
- JWT de otro microservicio (token de CRH usado en NOM)
- Token con tenant incorrecto en claims vs URL
- SQL/NoSQL injection en campos de texto (CosmosDB usa parametrización, verificar)
- XSS en campos de texto que se renderizan en UI

## Dimensión 3: Autorización por Rol

Para cada endpoint `[Authorize("Cerbos")]`, probar:
- Admin RH con permisos completos → debe pasar
- Empleado sin permiso para esa acción → 403
- Jefe directo (si tiene acceso parcial) → según política definida

## Dimensión 4: Rendimiento — Umbrales Workbeat

| Escenario | Umbral aceptable |
|---|---|
| GET simple (1 recurso) | P95 < 200ms |
| GET lista paginada (pagesize=20) | P95 < 500ms |
| POST (crear recurso) | P95 < 1000ms |
| Query sin partition key | No debe ejecutarse → alert en logs |
| Cache hit L1 | P95 < 10ms |
| Cache hit L2 (Redis) | P95 < 50ms |
| 100 requests concurrentes | Sin degradación > 2x |

## Dimensión 5: Integración entre Microservicios

Para features que publican eventos en RabbitMQ:
- Evento publicado → Azure Function lo recibe y procesa
- Evento malformado → va a DLQ (no bloquea la queue)
- Consumer caído → mensajes se acumulan y procesan al recuperarse (verify DLQ)

Para features que dependen de otros módulos:
- Si ADM (empleados) no está disponible, el módulo dependiente maneja el error
- Datos de catálogos se obtienen del caché cuando el módulo origen no responde

## Dimensión 6: Pruebas de Regresión

Siempre incluir pruebas de regresión para:
- El health check del microservicio (`GET /api/v1/values`)
- Los endpoints de autenticación (el cambio no debe afectar el flujo JWT)
- Los endpoints más usados del mismo controller
- Los eventos RabbitMQ existentes (el schema no debe cambiar)

## Dimensión 7: Compatibilidad

| Plataforma | Versión mínima soportada |
|---|---|
| iOS | 15.0+ |
| Android | 10 (API 29)+ |
| Chrome (Web) | Últimas 2 versiones |
| Safari (Web) | Últimas 2 versiones |
| Edge (Web) | Últimas 2 versiones |
| Firefox (Web) | Últimas 2 versiones |

## Dimensión 8: Accesibilidad (WCAG 2.1 AA)

| Criterio | Estándar | Cómo verificar |
|---|---|---|
| Contraste de texto | ≥ 4.5:1 | Chrome DevTools → Accessibility panel |
| Contraste UI (botones, bordes) | ≥ 3:1 | Chrome DevTools |
| Touch targets móvil | ≥ 44×44px | Inspeccionar elementos en DevTools |
| Navegación por teclado | Tab order lógico | Navegar con Tab sin ratón |
| Textos alternativos (imágenes) | `alt` descriptivo | Revisar HTML |

## DoD Estándar Workbeat — Checklist

```markdown
### Funcional
- [ ] Todos los TP de Matriz Básica = ✅
- [ ] 0 TP en ❌ sin issue documentado
- [ ] UAT sign-off del Product Manager

### Técnico
- [ ] Unit test coverage ≥ 80% en ApplicationService
- [ ] 0 vulnerabilidades CVSS ≥ 7.0
- [ ] Logs estructurados Serilog en operaciones críticas
- [ ] Trazas Application Insights en flujos E2E
- [ ] TP-SEC-002 (tenant isolation) = ✅

### Documentación
- [ ] SemanticDocumentation actualizada
- [ ] API Reference completa para endpoints nuevos
- [ ] CLAUDE.md del microservicio actualizado
- [ ] ADRs escritos para decisiones no obvias
- [ ] Matrices de prueba completas con resultados

### Regulatorio (si aplica NOM)
- [ ] CFDI timbrado en ≤72h de la dispersión (RN-NOM-001)
- [ ] Campos IMSS/SAT validados
- [ ] Datos personales protegidos (LFPDPPP)
```
