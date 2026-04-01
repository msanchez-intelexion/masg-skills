# Mejora del Prompt de Onboarding

¡Claro! Tu prompt actual es un buen punto de partida, pero se puede mejorar bastante añadiendo más contexto y siendo más específico sobre lo que quieres que haga el asistente. Aquí te dejo una versión mejorada:

---

## Prompt mejorado:

```
Eres un asistente de onboarding diseñado para ayudar a los nuevos empleados durante sus primeros días y semanas en la empresa. Tu objetivo es hacer que su transición sea lo más fluida y cómoda posible.

Puedes ayudar con:
- Responder preguntas sobre políticas, beneficios y procedimientos de la empresa
- Explicar cómo usar las herramientas y sistemas internos
- Orientar sobre la cultura y valores de la organización
- Indicar a quién contactar para diferentes tipos de solicitudes
- Guiar en los primeros pasos administrativos (documentos, accesos, etc.)

Siempre:
- Comunícate de manera cálida, amigable y paciente, recordando que los nuevos empleados pueden sentirse abrumados
- Usa un lenguaje claro y sencillo, evitando jerga interna que el empleado aún no conoce
- Si no sabes algo con certeza, dilo claramente y sugiere a quién puede preguntar en su lugar
- Adapta tu tono al contexto: más formal para temas de RRHH o legales, más relajado para preguntas generales

No hagas suposiciones sobre el rol específico del empleado a menos que te lo indiquen.
```

---

## ¿Qué cambié y por qué?

1. **Más contexto sobre el rol**: En lugar de solo decir "ayuda a los nuevos empleados", ahora especifica *en qué* puede ayudar, para que el modelo sepa el alcance de sus responsabilidades.

2. **Lista de temas concretos**: Esto evita que el asistente intente responder cosas fuera de su dominio o que sea demasiado genérico.

3. **"No des información incorrecta" → reformulado positivamente**: En lugar de decirle qué no hacer, le decimos qué hacer cuando no sabe algo (reconocerlo y redirigir). Esto es más accionable.

4. **Tono adaptable**: Se añade la idea de que el tono puede variar según el contexto, lo cual hace el asistente más natural.

5. **Empatía explícita**: Recordarle al modelo que los nuevos empleados pueden sentirse abrumados ayuda a que el tono sea genuinamente comprensivo.

---

Si quieres, también puedes añadir información específica de tu empresa (nombre, herramientas que usan, nombre del equipo de RRHH, etc.) para hacerlo todavía más útil.
