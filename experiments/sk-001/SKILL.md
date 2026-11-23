---
name: micv-candidatura-sync
description: Ejecutar en seco y auditar la sincronización de una candidatura MiCV desde Markdown canónico a Markdown y PDF candidatos, con QA, manifest y checkpoint. Usar cuando BIZB prepare o valide candidaturas sin publicar en GitHub o WordPress.
---

# MiCV Candidatura Sync — SK-001

## Contrato
Entrada: Markdown canónico aprobado y configuración JSON con hash, reglas de anonimización, controles y permisos. Salidas: candidate.md, candidate.pdf, qa-report.json, manifest.json y checkpoint.md.

## Flujo
1. Leer fuentes versionadas y registrar SHA-256 del Markdown. Comparar con source_sha256, cuando exista.
2. Preparar configuración de acuerdo con references/run-schema.md, siempre con publish=false y aprobación humana requerida.
3. Ejecutar: python scripts/dry_run.py --source INPUT.md --config run.json --output OUT.
4. Inspeccionar PDF, QA, advertencias de privacidad y hashes. Un fallo bloquea aceptación.
5. Registrar la evidencia y checkpoint. No publicar.
6. Comparar manualmente con WordPress; el script no dispone de adaptador HTTP.

## Restricciones
- Rechazar publicación y herramientas remotas.
- Diferenciar nombres visibles de nombres en URLs históricas.
- No equiparar presencia en CV con evidencia independiente de la afirmación.
- No estimar costes o tokens como si fueran medidos.
- PDF de ensayo distinto de PDF editorial final.
