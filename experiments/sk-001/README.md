# SK-001 — MiCV Candidatura Sync / ensayo E-001

Estado: prototipo probado localmente, no desplegado ni aprobado para producción.

## Finalidad
Generar Markdown y PDF candidatos, informe QA, manifiesto con hashes y checkpoint desde MiCV THINKIA validado. No modifica producción.

## Uso
Instalar reportlab y PyMuPDF en Python. Ejecutar: python scripts/dry_run.py --source cvs/cv-quique-villar-thinkia.md --config run.json --output out/

## Evidencias E-001
- 6 fortalezas, 7 misiones, 10 enlaces.
- PDF candidato de 2 páginas, Markdown candidato, QA PASS y 4 unit tests PASS.
- Advertencia: algunos slugs históricos contienen nombres de cliente.
- Enlaces verificados sintácticamente, no por HTTP.
- Sin publicación en WordPress ni cambios en main.
- Pruebas de permisos y hash rechazaron ejecuciones no autorizadas.

El Harness es mínimo y local. No constituye la plataforma BIZB completa.
