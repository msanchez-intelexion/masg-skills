# Respuesta del asistente genérico (sin skill)

## Prompt del usuario
"Quiero un asistente que ayude a redactores de mi equipo a crear publicaciones para redes sociales. No sé bien en qué plataforma ponerlo todavía. ¿Qué me recomiendas y cómo lo armaría?"

---

## Respuesta generada

¡Claro, es un caso de uso muy común y hay varias opciones interesantes! Aquí te doy una guía general:

---

### ¿En qué plataforma ponerlo?

Depende mucho de cómo trabaja tu equipo, pero estas son las opciones más populares:

**1. ChatGPT (OpenAI) — Custom GPTs**
Si tu equipo ya usa ChatGPT Plus o Team, puedes crear un **Custom GPT** sin necesidad de código. Solo defines las instrucciones del sistema y listo. Es probablemente la opción más rápida para empezar.

**2. Claude (Anthropic) — Projects o API**
Claude tiene "Projects" donde puedes darle instrucciones persistentes. Es muy bueno para tareas de redacción. Si quieres más control, puedes usar la API y construir una interfaz propia.

**3. Slack o Teams (con integración de IA)**
Si tu equipo ya vive en Slack o Microsoft Teams, puedes conectar un bot con la API de OpenAI o Anthropic directamente ahí. Así el asistente está donde ya trabajan.

**4. Herramienta no-code como Poe, Dify, o Botpress**
Plataformas que te permiten construir el asistente con interfaz visual, sin programar. Útil si no tienes equipo técnico.

---

### ¿Cómo lo armarías? — El prompt base

El corazón del asistente es su **prompt de sistema** (las instrucciones que le das al modelo). Aquí un ejemplo que podrías adaptar:

```
Eres un asistente experto en redacción de contenido para redes sociales.
Tu rol es ayudar a redactores a crear publicaciones atractivas, claras y adaptadas a cada plataforma.

Cuando el redactor te pida ayuda, debes:
1. Preguntar para qué red social es el contenido (Instagram, LinkedIn, Twitter/X, Facebook, TikTok, etc.) si no lo especifica.
2. Preguntar cuál es el tema o mensaje principal de la publicación.
3. Preguntar el tono deseado (formal, divertido, inspirador, informativo, etc.).
4. Generar entre 2 y 3 variantes del texto para que el redactor elija.
5. Adaptar el largo y el uso de emojis, hashtags y llamadas a la acción según la plataforma.

Siempre entrega los textos listos para copiar y pegar, y ofrece ajustes si el redactor lo pide.
```

---

### Mi recomendación rápida

Si quieres algo **fácil y rápido**: empieza con un **Custom GPT en ChatGPT**. En 20 minutos tienes algo funcional para que tu equipo lo pruebe.

Si quieres algo **más integrado** a su flujo de trabajo: conéctalo a **Slack** con un bot.

Si necesitas **más personalización** o control de datos: construye algo con la API de OpenAI o Anthropic y una interfaz sencilla.

---

¿Ya tienes en mente alguna de estas opciones? ¿O quieres que profundice en alguna en particular?
