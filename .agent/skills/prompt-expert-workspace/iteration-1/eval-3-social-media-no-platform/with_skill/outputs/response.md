# Respuesta del Prompt Expert — Eval #3 (WITH skill)

**Prompt del usuario:**
> "Quiero un asistente que ayude a redactores de mi equipo a crear publicaciones para redes sociales. No sé bien en qué plataforma ponerlo todavía. ¿Qué me recomiendas y cómo lo armaría?"

---

## Respuesta simulada (con skill activo)

Excelente caso de uso — un asistente para redactores de redes sociales tiene mucho potencial. Antes de diseñar el prompt, necesito completar el diagnóstico mínimo (**Fase A**) para que el resultado sea realmente efectivo.

Ya tengo dos datos clave de tu descripción:

- ✅ **Objetivo:** Ayudar a redactores a crear publicaciones para redes sociales
- ✅ **Público objetivo:** Redactores de tu equipo (usuarios internos, presumiblemente con conocimiento editorial)

Sin embargo, hay una pieza que es **obligatoria antes de continuar**:

---

### ⚠️ Pregunta crítica: ¿En qué plataforma vas a desplegarlo?

El diseño del prompt cambia significativamente según la plataforma. No puedo elegir una por defecto ni generar el prompt final sin saber esto. Las tres opciones son:

| Plataforma | Mejor para… | Consideración clave |
|------------|-------------|---------------------|
| **ChatGPT (GPT personalizado)** | Equipos que ya usan ChatGPT Plus o Enterprise; flujos con lógica "si-entonces" claros | Requiere suscripción; editor de GPTs es visual e intuitivo; ideal si quieres distribuirlo fácilmente dentro de tu organización |
| **Claude (claude.ai / API)** | Prompts con razonamiento estructurado y alta coherencia semántica; instrucciones complejas en XML | Excelente para tareas creativas con restricciones de tono y estilo; responde muy bien a instrucciones tipo "¿por qué?" |
| **Gemini (Gems / API)** | Integración con Google Workspace; redactores que ya trabajan en Google Docs/Drive | Fuerte integración con el ecosistema Google; proactividad comunicativa; responde bien a instrucciones en prosa |

**Mi recomendación preliminar:**

- Si tu equipo ya usa **Google Workspace** → considera Gemini (Gems)
- Si tu equipo usa **ChatGPT Plus o la empresa tiene licencia Enterprise** → ChatGPT GPTs es el camino más directo
- Si buscas la **mayor calidad de razonamiento y adherencia a un tono editorial específico** → Claude con etiquetas XML es el más preciso

---

### Mientras decides la plataforma, te hago dos preguntas más de la Fase A:

1. **Base de conocimiento:** ¿Los redactores van a proporcionar el tema libremente, o hay guías de estilo, listas de hashtags, ejemplos de publicaciones anteriores, o briefs de marca que el asistente debería conocer?

2. **Redes sociales objetivo:** ¿El asistente debe manejar múltiples redes (Instagram, LinkedIn, X/Twitter, TikTok) con sus propias convenciones, o se enfoca en una sola?

---

Una vez que me confirmes la **plataforma** (y opcionalmente las otras dos respuestas), paso directamente al **Razonamiento Estratégico (Fase B)** y te entrego el prompt completo listo para copiar y usar.
