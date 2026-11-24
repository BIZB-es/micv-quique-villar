# MiCV Portal — aislamiento multiusuario (MVP 0.1.2)

Estado: **desarrollo y prueba local; acceso real aún no autorizado**.

## Corrección del control de acceso
La versión 0.1.1 admitía a cualquier usuario con la capacidad base `read`. Esto incluye suscriptores ordinarios de WordPress. La versión 0.1.2 admite únicamente:
- administradores autorizados de MiCV (`manage_options`);
- usuarios con rol `micv_candidate`.

No basta con estar autenticado. Se mantienen comprobaciones de propiedad por ID de candidatura para acciones sensibles.

## Resultado local
Ocho comprobaciones PHP con WordPress simulado han pasado: listados separados para A/B; no se muestran notas ajenas; administrador puede revisar todos; control de aprobación solo administrativo; suscriptor normal rechazado; anónimo ve acceso de inicio de sesión. `php -l` pasa en la versión 0.1.2.

## Advertencias
- Los mocks no sustituyen pruebas HTTP con dos usuarios reales.
- El shortcode de la página de gestión (ID 525) permanece en borrador.
- No se han creado usuarios reales ni expedientes con información de terceros.
- No se deben incluir datos o fuentes personales en este repositorio público.
- La conexión de Google Drive de un administrador no demuestra segregación entre candidatos.
- Código fuente completo: paquete WordPress de implementación 0.1.2; pendiente introducirlo de forma íntegra en un repositorio de código, con CI de pruebas.

## Prueba P-MICV-MULTI-001 (pendiente)
1. Dos identidades ficticias con rol MiCV y una cuenta administradora.
2. Crear expedientes A y B en sesiones independientes.
3. Verificar lectura por propietario y rechazo HTTP 403 a manipulación de ID en save, request_review, archive y reopen.
4. Verificar que aprobar y registrar envío requieren administrador; edición revoca aprobaciones.
5. Validar CSRF, usuarios sin rol, enlaces permitidos, no publicación en REST/búsquedas y retención.
6. Registrar evidencia anonimizada y decidir apertura del portal solo cuando todos los controles críticos pasen.

## Criterio de cierre
No existe acceso cruzado ni modificación por ID de otro candidato. Ninguna aprobación o publicación externa sin revisión humana. Controles y evidencias reproducibles antes de invitar a personas reales.
