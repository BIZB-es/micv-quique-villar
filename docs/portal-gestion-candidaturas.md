# Portal MiCV — gestión de candidaturas (2026-11-24)

Estado: **prototipo de interfaz en WordPress, borrador**. No es todavía un sistema transaccional ni una zona privada multiusuario.

## Objetivo de producto
Cerrar el servicio de entropyme.biz como portal de gestión de candidaturas, empezando por un flujo acotado de contratación urgente.

## Orden de trabajo
1. Definir y terminar un objetivo concreto y verificable de producto.
2. Guardar lecciones aprendidas en Obsidian y código, pruebas y decisiones técnicas en GitHub.
3. Traducir los procedimientos repetibles en Skills y componentes de Harness BIZB.

## Lo implementado
- WordPress: página `Gestión de candidaturas | MiCV`, ID 525, slug `gestion-candidaturas`, **draft**.
- Contenido: inventario inicial de THINKIA, flujo de oportunidad a publicación, enlaces existentes y requisitos para operaciones reales.
- Sin escrituras en candidaturas ni mecanismo de autenticación por candidato.
- Caso THINKIA: candidatura v02.00 validada por el titular.

## BizDriver.ai: recomendación para MVP
No convertir el asistente en dependencia obligatoria. Mantener punto de integración opcional; habilitarlo solo cuando exista separación entre titulares, permisos, control de fuentes y evaluación de privacidad. **Recomendación pendiente de decisión formal.**

## Para pasar de interfaz a servicio
- Identidades y roles (titular, gestor, administrador).
- Entidades: candidato, oportunidad, candidatura, estado, versión, fuente, autorización y evento de auditoría.
- Operaciones reales de crear, actualizar, consultar, archivar y registrar seguimiento.
- Permisos servidor, aislamiento de expedientes y datos privados.
- Aprobación humana antes de enviar/publicar.
- Prueba con candidatura ficticia, plazo urgente y verificación de acceso cruzado.

## Criterio de aceptación
Un titular autorizado gestiona sus candidaturas y sus versiones sin acceso a datos de terceros; la publicación requiere aprobación y deja rastro auditable.

## Relación con IA agéntica
SK-001 y el Harness son herramientas auxiliares para generación y QA, no sustituyen el portal. Evitar expandir experimentos E-002 antes de contar con un flujo de producto funcional.

## Fuentes
- https://entropyme.biz/cv-quique-villar-thinkia/
- Obsidian/Drive: Portal-MiCV-gestion-candidaturas-20261124.md
- Rama de ensayo: `experiment/sk-001-micv-dry-run`
