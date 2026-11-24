# MiCV Portal v0.2.0 — Oportunidades y candidaturas

**Estado:** implementado en el plugin WordPress, pruebas PHP locales superadas, instalado y activo en entropyme.biz; interfaz página 525 todavía en borrador.

## Modelo
- `micv_opportunity`: registro privado por titular, estados `detected`, `evaluated`, `prioritized`, `discarded`.
- Campos de identificación: oportunidad, organización, URL HTTPS, confianza, notas de evidencia/riesgo, fecha de registro de fuente, y puntuaciones enteras de 0 a 5 para cinco factores.
- Pesos: encaje 30%, influencia 20%, impacto 20%, condiciones 15%, accesibilidad 15%. Total: suma `(nota/5) * peso`; escala 0–100.
- `micv_application`: registro privado por titular, se deriva solo de una oportunidad priorizada, mediante POST explícito confirmado; origen en `_micv_source_opportunity_id`.
- Máximo 9 candidaturas activas por titular; archivar libera capacidad; reabrir vuelve a comprobar límite.
- Una oportunidad ya convertida no puede originar una segunda candidatura, incluso si la primera está archivada. Editar la candidatura revoca aprobaciones existentes.
- Nada se publica ni envía automáticamente.

## Seguridad
- CPT privados; REST deshabilitado; controles por titular/administrador sobre las acciones y listado.
- Nonces en operaciones POST; los nombres visibles se escapan y las URL de fuente usan HTTPS.
- Las acciones de conversión verifican propiedad, estado priorizado, confirmación, límite y duplicados.
- Importante: la fuente y puntuación son datos aportados, no verificaciones de fuentes externas. No hay contacto autónomo.

## Pruebas locales (mocks)
- 8 pruebas anteriores de acceso y visibilidad: PASS.
- 16 comprobaciones nuevas sobre oportunidades: PASS; separación entre A/B, subscriptores, conversión exclusiva de oportunidad priorizada, propiedad, duplicados, confirmación explícita, límite 9, trazabilidad origen y estado borrador.
- PHP syntax: PASS.
- No se han realizado pruebas HTTP reales con dos sesiones ni una auditoría formal de seguridad. No habilitar aún a usuarios reales.
- El control del límite de 9 no es transaccional frente a peticiones concurrentes; endurecer antes de escalar.
- El registro de auditoría se limita a últimos 100 eventos; no es inmutable.

## Despliegue
- Plugin 0.2.0 confirmado activo en WordPress.
- Página 525 `gestion-candidaturas` sigue en `draft` y conserva shortcode `[micv_portal]`.
- El código del plugin no se ha incorporado todavía íntegramente a GitHub. Paquete local `micv-portal-v0.2.0.zip` disponible para mantener la trazabilidad del despliegue.
- No se crean automáticamente oportunidades históricas ni candidaturas THINKIA.

## Próximo control de aceptación
Con dos cuentas ficticias, crear oportunidades A y B, intentar acceder y modificar el expediente ajeno, evaluar/conversionar de forma explícita, verificar vínculo y estado, 10.ª candidatura activa bloqueada, y comprobar aprobación humana para envío.
