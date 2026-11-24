# MiCV Portal 0.3.0 — Agent Opportunity Intake

Estado: **código instalado y activo en entropyme.biz; endpoint pendiente de activación operativa por credenciales de agente**. Página del portal ID 525 sigue en borrador.

## Protocolo
`POST /wp-json/micv/v1/opportunities`

Autenticación: WordPress Application Password por HTTPS de un usuario dedicado con rol `micv_scout`. En el panel de WordPress: **Ajustes > MiCV Opportunity Scout**, indicar ID del titular destino. No usar claves de administrador ni insertar secretos en GitHub.

El servidor ignora cualquier `owner_id`, `state`, `approve` o `submit` enviado por un agente y solo permite crear oportunidades privadas en estado `detected`.

```json
{
  "external_id": "source:example-0001",
  "title": "Ejemplo sintético: dirección de transformación",
  "organization": "Organización ficticia",
  "source_url": "https://example.org/job/0001",
  "scores": {
    "fit": 4,
    "influence": 4,
    "impact": 5,
    "conditions": 3,
    "access": 5
  },
  "rationale": "Ejemplo, no una oferta real",
  "agent_version": "scout/0.1"
}
```

Respuesta 201: creación; 200: duplicado por `external_id` dentro del mismo titular. Errores: 400 (validación), 401 (sin autenticación), 403 (sin rol agente), 503 (titular no configurado).

## Evaluación y decisión
`score_total = sum(score_i * weight_i / 5)`; pesos 30/20/20/15/15. Toda puntuación del agente es una propuesta revisable. La confianza permanece `pendiente` hasta validación humana. El titular puede priorizar, investigar, descartar y solo convertir explícitamente a candidatura bajo las reglas anteriores: máximo nueve activas, vínculo al origen, sin duplicación.

## QA
- 14 pruebas mock locales API: PASS, incluyendo autorización de rol, propiedad, rechazo de HTTP/IP, rangos 0–5, idempotencia, estado detectado y negativa de suplantación.
- Regresión previa de permisos y oportunidades: PASS; PHP lint PASS.
- **No hay todavía test autenticado HTTP de extremo a extremo ni agente conectado.** El conector de WordPress no invoca endpoints REST personalizados.
- La deduplicación no es aún transaccional para peticiones concurrentes y el historial de eventos es limitado. Endurecer antes de puesta en servicio abierta.
- No publicar información personal ni credenciales en este repositorio.

## Despliegue y pruebas de aceptación pendientes
1. Crear cuenta técnica y Application Password mediante la interfaz administrativa; titular definido explícitamente.
2. POST de propuesta sintética con código 201; reenvío de igual `external_id` => 200 duplicate.
3. Confirmar bandeja privada, separación de usuarios, cambio de estado por titular y bloqueo de conversión autónoma.
4. Procesar una primera selección de cinco ofertas verificadas y registrar decisiones y aprendizajes.

Código: paquete `micv-portal-v0.3.0.zip`; el versionado íntegro de la fuente del plugin sigue pendiente.
