# Benchmark — prompt-expert · Iteración 1

## Resumen ejecutivo

| Configuración  | Eval 1 (ChatGPT) | Eval 2 (Claude) | Eval 3 (sin plataforma) | **Promedio** |
|----------------|:----------------:|:---------------:|:------------------------:|:------------:|
| **Con skill**  | 7/7 — 100%       | 6/6 — 100%      | 4/4 — 100%               | **100%**     |
| **Sin skill**  | 0/7 — 0%         | 2/6 — 33%       | 1/4 — 25%                | **19%**      |
| **Delta**      | +100%            | +67%            | +75%                     | **+81%**     |

---

## Resultados detallados

### Eval 1 — Asistente de atención a clientes (ChatGPT)

**Con skill — 7/7 ✅**

| Assertion | Resultado |
|-----------|-----------|
| Incluye Razonamiento Estratégico antes del prompt | ✅ |
| Usa delimitadores de ChatGPT (###, """, ---) | ✅ |
| Contiene ejemplos Input/Output (Few-Shot) | ✅ (2 ejemplos) |
| Incluye cláusula anti-leaking | ✅ (sección CONFIDENCIALIDAD) |
| Usa cuantificadores concretos | ✅ ("máx. 3 oraciones", "2-4 pasos") |
| Respuesta en bloque de código Markdown | ✅ |
| Framework PTCF presente | ✅ |

**Sin skill — 0/7 ❌** — Prosa genérica sin estructura, sin ejemplos, sin anti-leaking, sin cuantificadores.

---

### Eval 2 — Mejora de prompt de onboarding (Claude)

**Con skill — 6/6 ✅**

| Assertion | Resultado |
|-----------|-----------|
| Identifica problemas del prompt original | ✅ (9 gaps listados) |
| Usa etiquetas XML para Claude | ✅ (`<persona>`, `<tarea>`, `<contexto>`, `<formato>`, `<ejemplos>`, `<restricciones>`) |
| Convierte negativos a positivos | ✅ ("No des info incorrecta" → auto-verificación) |
| Agrega cuantificadores | ✅ (150 palabras, 1 emoji, 90 días) |
| Incluye Razonamiento Estratégico | ✅ (5 secciones) |
| Incluye cláusula anti-leaking | ✅ |

**Sin skill — 2/6** — Identifica problemas y convierte negativos naturalmente, pero sin XML, sin cuantificadores, sin razonamiento estratégico ni anti-leaking.

---

### Eval 3 — Asistente de redes sociales (plataforma no definida)

**Con skill — 4/4 ✅** — Bloqueó correctamente la generación del prompt; preguntó por la plataforma con tabla comparativa de las 3 opciones.

**Sin skill — 1/4** — Generó prompt directamente sin preguntar; no aplicó Fase A de diagnóstico.

---

## Análisis

### Fortalezas del skill
- **100% pass rate** en los 3 escenarios vs 19% baseline
- La **regla crítica de plataforma** funciona perfectamente (Eval 3)
- Genera **prompts production-ready** con todas las directivas operativas
- El **Razonamiento Estratégico** está presente y estructurado en todos los casos

### Observación sobre assertions
- En Eval 2, el baseline pasa 2/6 assertions naturalmente (identifica problemas + convierte negativos). Estas 2 son menos discriminativas; se podrían refinar para medir calidad más profunda.
- La assertion "presenta opciones de plataforma" pasa en ambas configuraciones del Eval 3 — el baseline también menciona plataformas, pero sin estructura. Se podría refinar a "presenta tabla comparativa estructurada".

### Estado del skill
✅ **Listo para producción** — Sin hallazgos críticos. El skill supera el baseline en +81 puntos porcentuales.
