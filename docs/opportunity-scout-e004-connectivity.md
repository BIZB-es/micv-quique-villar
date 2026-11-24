# E-004 — Integración Opportunity Scout: estado de conexión

Fecha: 2026-11-24. MiCV Portal 0.3.0 instalado y activo, pero aún NO recibe propuestas de un agente externo en entorno real.

## Comprobaciones
- Código del plugin: endpoint `POST /wp-json/micv/v1/opportunities`, autenticado con identidad `micv_scout`; titular configurado exclusivamente en servidor.
- La pantalla `Ajustes > MiCV Opportunity Scout` exige administrador y un POST con nonce para asignar destinatario.
- El acceso de los conectores WordPress disponibles no permite crear un usuario con rol propio, generar su Application Password o operar esa pantalla administrativa.
- El entorno local no resuelve `entropyme.biz`; por tanto, **no hubo petición HTTP de extremo a extremo ni inserción real**.
- No se usaron credenciales administrativas como agente, no se publicó la página 525 y no se enviaron mensajes/candidaturas.

## Entregable local
`micv-opportunity-scout-client.zip`: `submit.py` (cliente Python sin dependencias), `proposals.json` (cinco propuestas iniciales), `README.md` (procedimiento de alta). Solo dry-run realizado; cinco registros validados, puntuaciones 87/88/91/77/75. Aún deben verificarse vigencia y condiciones de las ofertas.

## Camino de aceptación
1. En WordPress: configurar ID titular en Ajustes → MiCV Opportunity Scout; usuario exclusivo con rol `micv_scout`, contraseña de aplicación (guardar fuera de chat).
2. Ejecutar una prueba sintética `201 created`; repetir el mismo `external_id`, esperando `200 duplicate`.
3. Verificar bandeja privada y rechazo de acceso cruzado con dos sesiones de candidato.
4. Solo entonces ingresar propuestas reales y revisar vigencia/condiciones.

**Principio**: la automatización solo propone. Priorizar y convertir a candidatura requiere decisión del titular. Nunca usar el administrador ni publicar claves para superar una limitación de acceso.
